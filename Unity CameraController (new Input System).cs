using UnityEngine;
using UnityEngine.InputSystem;

namespace Assets.Scripts.Keystrokes
{
    public class KeystrokesController : MonoBehaviour
    {
        [SerializeField] private float cameraDragSpeed;
        [SerializeField] private float cameraSpeed;
        [SerializeField] private float zoomSpeed;
        private InputAction _cameraDrag;
        private InputAction _cameraMovement;
        private global::Keystrokes _keystrokes;
        private bool _rightClickPressed;
        private Rigidbody _rigidbody;

        private void Awake()
        {
            //init input system
            _keystrokes = new global::Keystrokes();
            _rigidbody = gameObject.GetComponent<Rigidbody>();
        }

        private void FixedUpdate()
        {
            //camera movement script
            var movement = _cameraMovement.ReadValue<Vector3>() * cameraSpeed;
            var direction = transform.rotation * Vector3.forward;
            _rigidbody.AddForce(Quaternion.FromToRotation(Vector3.forward,
                                    new Vector3(direction.x, 0, direction.z)
                                        .normalized) *
                                movement);
        }

        private void LateUpdate()
        {
            //camera zoom script
            _rigidbody.AddRelativeForce(Vector3.forward * Time.deltaTime * zoomSpeed *
                                        -Mouse.current.scroll.ReadValue().y);


            //camera drag rotation script
            if (_rightClickPressed)
            {
                var x = Mouse.current.delta.x.ReadValue() * cameraDragSpeed;
                var y = Mouse.current.delta.y.ReadValue() * cameraDragSpeed;

                if (Mathf.Abs(Utils.WrapAngle(transform.eulerAngles.x - y)) > 80) y = 0;
                var eulerAngles = transform.eulerAngles;
                eulerAngles =
                    Vector3.Lerp(eulerAngles, eulerAngles + new Vector3(-y, x, 0), 2f);
                transform.eulerAngles = eulerAngles;
            }
        }

        private void OnEnable()
        {
            EnableCamera();
        }

        private void OnDisable()
        {
            DisableCamera();
        }

        private void EnableCamera()
        {
            //enabling input system, hooking events
            _cameraMovement = _keystrokes.Camera.Movement;
            _cameraMovement.Enable();

            _cameraDrag = _keystrokes.Camera.Drag;
            _keystrokes.Camera.Drag.performed += OnRightClick;
            _keystrokes.Camera.Drag.canceled += OnNotRightClick;
            _cameraDrag.Enable();
        }

        private void OnNotRightClick(InputAction.CallbackContext obj)
        {
            _rightClickPressed = false;
        }

        private void OnRightClick(InputAction.CallbackContext obj)
        {
            _rightClickPressed = true;
        }

        private void DisableCamera()
        {
            //disabling input system
            _cameraMovement.Disable();

            _cameraDrag.performed -= OnRightClick;
            _cameraDrag.Disable();
        }
    }
}