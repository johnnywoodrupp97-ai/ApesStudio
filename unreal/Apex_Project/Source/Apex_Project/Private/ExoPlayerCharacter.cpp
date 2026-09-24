#include "ExoPlayerCharacter.h"
#include "Apex_Project.h"
#include "ExoTypes.h"
#include "ExoVitalsComponent.h"
#include "ExoBuildComponent.h"
#include "ExoInteractable.h"
#include "ExoNoiseSubsystem.h"
#include "ExoMissionSubsystem.h"
#include "ExoGameMode.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SpotLightComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "InputModifiers.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "Engine/LocalPlayer.h"

AExoPlayerCharacter::AExoPlayerCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	GetCapsuleComponent()->InitCapsuleSize(35.f, 90.f); // 0.35 m radius, 1.8 m tall (level bible 02)

	Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
	Camera->SetupAttachment(GetCapsuleComponent());
	Camera->SetRelativeLocation(FVector(0.f, 0.f, 72.f)); // eye height ~1.62 m
	Camera->bUsePawnControlRotation = true;
	Camera->SetFieldOfView(90.f);

	HelmetLight = CreateDefaultSubobject<USpotLightComponent>(TEXT("HelmetLight"));
	HelmetLight->SetupAttachment(Camera);
	HelmetLight->SetIntensity(5000.f);
	HelmetLight->SetAttenuationRadius(2500.f);
	HelmetLight->SetOuterConeAngle(32.f);
	HelmetLight->SetVisibility(false);

	Vitals = CreateDefaultSubobject<UExoVitalsComponent>(TEXT("Vitals"));
	Build = CreateDefaultSubobject<UExoBuildComponent>(TEXT("Build"));

	UCharacterMovementComponent* Move = GetCharacterMovement();
	Move->MaxWalkSpeed = ExoTuning::JogSpeed;
	Move->MaxWalkSpeedCrouched = ExoTuning::CrouchSpeed;
	Move->JumpZVelocity = 340.f;  // ~0.6 m standing jump
	Move->MaxStepHeight = 45.f;   // 0.45 m step
	Move->SetWalkableFloorAngle(45.f);
	Move->GetNavAgentPropertiesRef().bCanCrouch = true;
	bUseControllerRotationYaw = true;
}

void AExoPlayerCharacter::BeginPlay()
{
	Super::BeginPlay();
	Vitals->OnDied.AddDynamic(this, &AExoPlayerCharacter::OnVitalsDied);
}

void AExoPlayerCharacter::OnVitalsDied()
{
	if (AExoGameMode* GM = GetWorld()->GetAuthGameMode<AExoGameMode>())
	{
		GM->HandlePlayerDeath(this);
	}
}

UInputAction* AExoPlayerCharacter::MakeAction(FName Name, bool bAxis2D)
{
	UInputAction* A = NewObject<UInputAction>(this, Name);
	A->ValueType = bAxis2D ? EInputActionValueType::Axis2D : EInputActionValueType::Boolean;
	Actions.Add(A);
	return A;
}

void AExoPlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	UEnhancedInputComponent* Input = Cast<UEnhancedInputComponent>(PlayerInputComponent);
	if (!Input)
	{
		UE_LOG(LogExodus, Error, TEXT("Enhanced Input is required (Config/DefaultInput.ini)"));
		return;
	}
	Mapping = NewObject<UInputMappingContext>(this, TEXT("IMC_Exodus"));

	UInputAction* MoveA = MakeAction(TEXT("IA_Move"), true);
	UInputAction* LookA = MakeAction(TEXT("IA_Look"), true);
	auto Button = [this](const TCHAR* Name, FKey Key)
	{
		UInputAction* A = MakeAction(FName(Name), false);
		Mapping->MapKey(A, Key);
		return A;
	};

	// WASD -> 2D axis: W = +Y, S = -Y, D = +X, A = -X.
	{
		FEnhancedActionKeyMapping& W = Mapping->MapKey(MoveA, EKeys::W);
		W.Modifiers.Add(NewObject<UInputModifierSwizzleAxis>(this));
		FEnhancedActionKeyMapping& S = Mapping->MapKey(MoveA, EKeys::S);
		S.Modifiers.Add(NewObject<UInputModifierSwizzleAxis>(this));
		S.Modifiers.Add(NewObject<UInputModifierNegate>(this));
		Mapping->MapKey(MoveA, EKeys::D);
		FEnhancedActionKeyMapping& A = Mapping->MapKey(MoveA, EKeys::A);
		A.Modifiers.Add(NewObject<UInputModifierNegate>(this));
		Mapping->MapKey(MoveA, EKeys::Gamepad_Left2D);
		Mapping->MapKey(LookA, EKeys::Mouse2D);
		Mapping->MapKey(LookA, EKeys::Gamepad_Right2D);
	}

	Input->BindAction(MoveA, ETriggerEvent::Triggered, this, &AExoPlayerCharacter::Move);
	Input->BindAction(LookA, ETriggerEvent::Triggered, this, &AExoPlayerCharacter::Look);

	UInputAction* Sprint = Button(TEXT("IA_Sprint"), EKeys::LeftShift);
	Mapping->MapKey(Sprint, EKeys::Gamepad_LeftThumbstick);
	Input->BindAction(Sprint, ETriggerEvent::Started, this, &AExoPlayerCharacter::StartSprint);
	Input->BindAction(Sprint, ETriggerEvent::Completed, this, &AExoPlayerCharacter::StopSprint);

	UInputAction* CrouchA = Button(TEXT("IA_Crouch"), EKeys::LeftControl);
	Mapping->MapKey(CrouchA, EKeys::Gamepad_FaceButton_Right);
	Input->BindAction(CrouchA, ETriggerEvent::Started, this, &AExoPlayerCharacter::ToggleCrouch);

	UInputAction* JumpA = Button(TEXT("IA_Jump"), EKeys::SpaceBar);
	Mapping->MapKey(JumpA, EKeys::Gamepad_FaceButton_Bottom);
	Input->BindAction(JumpA, ETriggerEvent::Started, this, &AExoPlayerCharacter::DoJump);

	UInputAction* PrimaryA = Button(TEXT("IA_Primary"), EKeys::LeftMouseButton);
	Mapping->MapKey(PrimaryA, EKeys::Gamepad_RightTrigger);
	Input->BindAction(PrimaryA, ETriggerEvent::Started, this, &AExoPlayerCharacter::Primary);
	Input->BindAction(PrimaryA, ETriggerEvent::Completed, this, &AExoPlayerCharacter::PrimaryReleased);

	UInputAction* SecondaryA = Button(TEXT("IA_Secondary"), EKeys::RightMouseButton);
	Mapping->MapKey(SecondaryA, EKeys::Gamepad_LeftTrigger);
	Input->BindAction(SecondaryA, ETriggerEvent::Started, this, &AExoPlayerCharacter::Secondary);
	Input->BindAction(SecondaryA, ETriggerEvent::Completed, this, &AExoPlayerCharacter::SecondaryReleased);

	UInputAction* InteractA = Button(TEXT("IA_Interact"), EKeys::E);
	Mapping->MapKey(InteractA, EKeys::Gamepad_FaceButton_Left);
	Input->BindAction(InteractA, ETriggerEvent::Started, this, &AExoPlayerCharacter::Interact);

	UInputAction* BuildA = Button(TEXT("IA_Build"), EKeys::B);
	Mapping->MapKey(BuildA, EKeys::Gamepad_DPad_Up);
	Input->BindAction(BuildA, ETriggerEvent::Started, this, &AExoPlayerCharacter::ToggleBuild);

	UInputAction* RotateA = Button(TEXT("IA_Rotate"), EKeys::R);
	Input->BindAction(RotateA, ETriggerEvent::Started, this, &AExoPlayerCharacter::RotatePart);

	UInputAction* NextA = Button(TEXT("IA_NextPart"), EKeys::MouseScrollUp);
	Mapping->MapKey(NextA, EKeys::Gamepad_RightShoulder);
	Input->BindAction(NextA, ETriggerEvent::Started, this, &AExoPlayerCharacter::CyclePart);

	UInputAction* LightA = Button(TEXT("IA_HelmetLight"), EKeys::L);
	Mapping->MapKey(LightA, EKeys::Gamepad_DPad_Right);
	Input->BindAction(LightA, ETriggerEvent::Started, this, &AExoPlayerCharacter::ToggleLight);

	UInputAction* MedA = Button(TEXT("IA_Suppressant"), EKeys::H);
	Mapping->MapKey(MedA, EKeys::Gamepad_DPad_Left);
	Input->BindAction(MedA, ETriggerEvent::Started, this, &AExoPlayerCharacter::UseSuppressant);

	UInputAction* SkipA = Button(TEXT("IA_SkipLine"), EKeys::Enter);
	Input->BindAction(SkipA, ETriggerEvent::Started, this, &AExoPlayerCharacter::SkipLine);

	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (ULocalPlayer* LP = PC->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Sub = LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
			{
				Sub->AddMappingContext(Mapping, 0);
			}
		}
	}
}

void AExoPlayerCharacter::Move(const FInputActionValue& Value)
{
	if (!bInputEnabled) return;
	const FVector2D V = Value.Get<FVector2D>();
	const FRotator Yaw(0.f, GetControlRotation().Yaw, 0.f);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::X), V.Y);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::Y), V.X);
}

void AExoPlayerCharacter::Look(const FInputActionValue& Value)
{
	const FVector2D V = Value.Get<FVector2D>();
	AddControllerYawInput(V.X);
	AddControllerPitchInput(-V.Y);
}

void AExoPlayerCharacter::StartSprint(const FInputActionValue& Value) { bSprinting = true; }
void AExoPlayerCharacter::StopSprint(const FInputActionValue& Value) { bSprinting = false; }

void AExoPlayerCharacter::ToggleCrouch(const FInputActionValue& Value)
{
	if (bIsCrouched) UnCrouch(); else Crouch();
}

void AExoPlayerCharacter::DoJump(const FInputActionValue& Value)
{
	if (bInputEnabled) Jump();
}

void AExoPlayerCharacter::Primary(const FInputActionValue& Value)
{
	if (!bInputEnabled) return;
	bPrimaryHeld = true;
	if (Build->IsBuildMode())
	{
		Build->PrimaryPressed();
	}
	else
	{
		SwingWrench();
	}
}

void AExoPlayerCharacter::PrimaryReleased(const FInputActionValue& Value) { bPrimaryHeld = false; }
void AExoPlayerCharacter::Secondary(const FInputActionValue& Value) { bSecondaryHeld = true; }
void AExoPlayerCharacter::SecondaryReleased(const FInputActionValue& Value) { bSecondaryHeld = false; }

void AExoPlayerCharacter::Interact(const FInputActionValue& Value)
{
	if (!bInputEnabled) return;
	if (AActor* Target = FocusActor.Get())
	{
		if (IExoInteractable* I = Cast<IExoInteractable>(Target))
		{
			if (I->CanInteract(this)) I->Interact(this);
		}
	}
}

void AExoPlayerCharacter::ToggleBuild(const FInputActionValue& Value)
{
	if (bInputEnabled) Build->SetBuildMode(!Build->IsBuildMode());
}

void AExoPlayerCharacter::RotatePart(const FInputActionValue& Value) { Build->RotateGhost(); }
void AExoPlayerCharacter::CyclePart(const FInputActionValue& Value) { Build->CyclePart(1); }

void AExoPlayerCharacter::ToggleLight(const FInputActionValue& Value)
{
	HelmetLight->SetVisibility(!HelmetLight->IsVisible());
}

void AExoPlayerCharacter::UseSuppressant(const FInputActionValue& Value)
{
	Vitals->UseSuppressant();
}

void AExoPlayerCharacter::SkipLine(const FInputActionValue& Value)
{
	if (UExoMissionSubsystem* M = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
	{
		M->SkipDialogueLine();
	}
}

bool AExoPlayerCharacter::TraceView(float DistanceCm, FHitResult& OutHit) const
{
	const FVector Start = Camera->GetComponentLocation();
	const FVector End = Start + Camera->GetForwardVector() * DistanceCm;
	FCollisionQueryParams Params(SCENE_QUERY_STAT(ExoView), false, this);
	if (Build && Build->GetGhost())
	{
		Params.AddIgnoredActor(Build->GetGhost());
	}
	return GetWorld()->LineTraceSingleByChannel(OutHit, Start, End, ECC_Visibility, Params);
}

void AExoPlayerCharacter::SwingWrench()
{
	if (WrenchCooldown > 0.f || !Vitals->SpendStamina(ExoTuning::MeleeStaminaCost)) return;
	WrenchCooldown = 60.f / 70.f; // 70 swings per minute (22.7)
	FHitResult Hit;
	const FVector Start = Camera->GetComponentLocation();
	const FVector End = Start + Camera->GetForwardVector() * ExoTuning::WrenchRange;
	FCollisionQueryParams Params(SCENE_QUERY_STAT(ExoWrench), false, this);
	if (GetWorld()->SweepSingleByChannel(Hit, Start, End, FQuat::Identity, ECC_Pawn, FCollisionShape::MakeSphere(20.f), Params))
	{
		if (AActor* Victim = Hit.GetActor())
		{
			// Head hits (upper 20% of the target) use the weak-point multiplier, applied by the Hollow.
			UGameplayStatics::ApplyPointDamage(Victim, ExoTuning::WrenchDamage, Camera->GetForwardVector(), Hit, GetController(), this, nullptr);
		}
	}
	if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
	{
		Noise->ReportNoise(GetActorLocation(), ExoTuning::WrenchNoiseRadiusM, this, TEXT("Melee"));
	}
}

FText AExoPlayerCharacter::GetFocusPrompt() const
{
	if (const AActor* Target = FocusActor.Get())
	{
		if (const IExoInteractable* I = Cast<IExoInteractable>(Target))
		{
			return I->GetPrompt();
		}
	}
	return FText::GetEmpty();
}

void AExoPlayerCharacter::UpdateFocus()
{
	FocusActor = nullptr;
	FHitResult Hit;
	if (TraceView(250.f, Hit) && Hit.GetActor() && Hit.GetActor()->Implements<UExoInteractable>())
	{
		FocusActor = Hit.GetActor();
	}
}

void AExoPlayerCharacter::EmitMovementNoise(float DeltaSeconds)
{
	NoiseClock += DeltaSeconds;
	if (NoiseClock < 0.5f) return;
	NoiseClock = 0.f;
	const float Speed = GetVelocity().Size2D();
	if (Speed < 50.f || bIsCrouched) return; // crouch-walking is silent (level bible 12)
	const float Radius = bSprinting ? 15.f : (Speed > ExoTuning::WalkSpeed + 20.f ? 8.f : 5.f);
	if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
	{
		Noise->ReportNoise(GetActorLocation(), Radius, this, TEXT("Footsteps"));
	}
}

void AExoPlayerCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	WrenchCooldown = FMath::Max(0.f, WrenchCooldown - DeltaSeconds);

	// Sprinting costs 12 stamina/s; out of stamina, drop to a jog.
	const bool bMoving = GetVelocity().Size2D() > 50.f;
	bool bSprintNow = bSprinting && bMoving && !bIsCrouched && Vitals->Stamina > 1.f;
	if (bSprintNow && !Vitals->SpendStamina(ExoTuning::SprintStaminaPerSec * DeltaSeconds)) bSprintNow = false;
	GetCharacterMovement()->MaxWalkSpeed = bSprintNow ? ExoTuning::SprintSpeed : ExoTuning::JogSpeed;
	Vitals->bExerting = bSprintNow;

	if (Build->IsBuildMode())
	{
		if (bPrimaryHeld) Build->Weld(DeltaSeconds);
		if (bSecondaryHeld) Build->Grind(DeltaSeconds);
	}
	UpdateFocus();
	EmitMovementNoise(DeltaSeconds);
}

float AExoPlayerCharacter::TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser)
{
	const float Applied = Super::TakeDamage(Damage, DamageEvent, EventInstigator, DamageCauser);
	Vitals->ApplyDamage(Damage);
	return Applied;
}
