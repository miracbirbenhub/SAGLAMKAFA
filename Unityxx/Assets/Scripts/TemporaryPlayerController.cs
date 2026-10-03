using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(CharacterController))]
public sealed class TemporaryPlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float walkSpeed = 7.0f;
    [SerializeField] private float runSpeed = 12.0f;
    [SerializeField] private float jumpHeight = 4.0f;
    [SerializeField] private float gravity = -24.0f;

    [Header("Camera")]
    [SerializeField] private float mouseSensitivity = 0.10f;
    [SerializeField] private float minPitch = -15.0f;
    [SerializeField] private float maxPitch = 55.0f;

    public Transform CameraTransform { private get; set; }
    public Camera Camera { private get; set; }

    private CharacterController characterController;
    private float verticalVelocity;
    private float yaw;
    private float pitch = 16.0f;

    private void Awake()
    {
        characterController = GetComponent<CharacterController>();
        yaw = transform.eulerAngles.y;

        if (CameraTransform == null)
            CameraTransform = GetComponentInChildren<Camera>()?.transform;

        if (Camera == null && CameraTransform != null)
            Camera = CameraTransform.GetComponent<Camera>();
    }

    private void Start()
    {
        LockCursor(true);
    }

    private void Update()
    {
        HandleLook();
        HandleMovement();

        if (Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame)
            LockCursor(false);

        if (Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame)
            LockCursor(true);

        if (Camera != null && CameraTransform != null)
        {
            CameraTransform.localRotation = Quaternion.Euler(pitch, 0.0f, 0.0f);
        }
    }

    private void HandleLook()
    {
        if (Mouse.current == null || Cursor.lockState != CursorLockMode.Locked)
            return;

        Vector2 delta = Mouse.current.delta.ReadValue();
        yaw += delta.x * mouseSensitivity;
        pitch -= delta.y * mouseSensitivity;
        pitch = Mathf.Clamp(pitch, minPitch, maxPitch);

        transform.rotation = Quaternion.Euler(0.0f, yaw, 0.0f);
    }

    private void HandleMovement()
    {
        Vector2 input = Vector2.zero;

        if (Keyboard.current != null)
        {
            input = new Vector2(
                (Keyboard.current.dKey.isPressed ? 1.0f : 0.0f) -
                (Keyboard.current.aKey.isPressed ? 1.0f : 0.0f),
                (Keyboard.current.wKey.isPressed ? 1.0f : 0.0f) -
                (Keyboard.current.sKey.isPressed ? 1.0f : 0.0f));
        }

        input = Vector2.ClampMagnitude(input, 1.0f);

        Vector3 direction = transform.forward * input.y + transform.right * input.x;
        float speed = Keyboard.current != null && Keyboard.current.leftShiftKey.isPressed
            ? runSpeed
            : walkSpeed;

        if (characterController.isGrounded)
        {
            if (verticalVelocity < 0.0f)
                verticalVelocity = -2.0f;

            if (Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame)
                verticalVelocity = Mathf.Sqrt(jumpHeight * -2.0f * gravity);
        }

        verticalVelocity += gravity * Time.deltaTime;

        Vector3 velocity = direction * speed;
        velocity.y = verticalVelocity;

        characterController.Move(velocity * Time.deltaTime);
    }

    private void LockCursor(bool locked)
    {
        Cursor.lockState = locked ? CursorLockMode.Locked : CursorLockMode.None;
        Cursor.visible = !locked;
    }

    private void OnGUI()
    {
        GUI.Box(new Rect(12, 12, 320, 82), GUIContent.none);
        GUI.Label(new Rect(24, 22, 300, 24), "Pyungmoo - Geçici Karakter");
        GUI.Label(new Rect(24, 44, 300, 22), "WASD: Hareket   Shift: Koş   Space: Zıpla");
        GUI.Label(new Rect(24, 66, 300, 22), "Mouse: Kamera   ESC: İmleci bırak");
    }
}
