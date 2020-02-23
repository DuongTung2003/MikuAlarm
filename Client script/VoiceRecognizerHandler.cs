using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using KKSpeech;
using TMPro;

public class VoiceRecognizerHandler : MonoBehaviour
{

    public Button startRecordingButton;
    public TextMeshProUGUI resultText;
    public bool Recording;
    public Animator animator;
    public GameObject listenUI;
    public Weather_control weather_script;
    public MikuController MKcontroller;
    public Light_controller light_;
    void Start()
    {
        if (SpeechRecognizer.ExistsOnDevice())
        {
            SpeechRecognizerListener listener = GameObject.FindObjectOfType<SpeechRecognizerListener>();
            listener.onAuthorizationStatusFetched.AddListener(OnAuthorizationStatusFetched);
            listener.onAvailabilityChanged.AddListener(OnAvailabilityChange);
            listener.onErrorDuringRecording.AddListener(OnError);
            listener.onErrorOnStartRecording.AddListener(OnError);
            listener.onFinalResults.AddListener(OnFinalResult);
            listener.onPartialResults.AddListener(OnPartialResult);
            listener.onEndOfSpeech.AddListener(OnEndOfSpeech);
            startRecordingButton.enabled = false;
            SpeechRecognizer.RequestAccess();
        }
        else
        {
            resultText.text = "Sorry, but this device doesn't support speech recognition";
            startRecordingButton.enabled = false;
        }

    }

    public void OnFinalResult(string result)
    {
        resultText.text = result;
        animator.SetBool("Recording", false);
        SpeechRecognizer.StopIfRecording();
        Recording = false;
        Command(result);
        MKcontroller.interacted = true;
    }

    public void OnPartialResult(string result)
    {
        resultText.text = result;
        MKcontroller.interacted = true;
    }

    public void OnAvailabilityChange(bool available)
    {
        startRecordingButton.enabled = available;
        if (!available)
        {
            resultText.text = "Speech Recognition not available";
        }
        else
        {
            resultText.text = "Say something :)";
        }
    }

    public void OnAuthorizationStatusFetched(AuthorizationStatus status)
    {
        switch (status)
        {
            case AuthorizationStatus.Authorized:
                startRecordingButton.enabled = true;
                break;
            default:
                startRecordingButton.enabled = false;
                resultText.text = "Cannot use Speech Recognition, authorization status is " + status;
                break;
        }
    }

    public void OnEndOfSpeech()
    {
        // startRecordingButton.GetComponentInChildren<Text>().text = "Start Recording";
        animator.SetBool("Recording", false);
        SpeechRecognizer.StopIfRecording();
        Recording = false;
    }

    public void OnError(string error)
    {
        Debug.LogError(error);
        resultText.text = "Something went wrong... Try again! \n [" + error + "]";
        startRecordingButton.GetComponentInChildren<Text>().text = "Start Recording";
        animator.SetBool("Recording", false);
        Recording = false;
    }

    public void OnStartRecordingPressed()
    {
        if (SpeechRecognizer.IsRecording())
        {
            listenUI.SetActive(false);
            animator.SetBool("Recording", false);
            SpeechRecognizer.StopIfRecording();
            startRecordingButton.GetComponentInChildren<Text>().text = "Start Recording";
            Recording = false;
        }
        else
        {
            listenUI.SetActive(true);
            Recording = true;
            animator.SetBool("Recording", true);
            SpeechRecognizer.StartRecording(true);
            startRecordingButton.GetComponentInChildren<Text>().text = "Stop Recording";
            resultText.text = "Say something :)";
           
        }
    }
    private void Command(string data)
    {
        bool B = true;
        foreach (string item in data.Split(' '))
        {
            switch (item.ToLower())
            {
                case "weather":
                    weather_script.request_data();
                    break;
                case "hi":
                    MKcontroller.Hi();
                    break;
                case "hello":
                    MKcontroller.Hi();
                    break;
                case "light":
                    light_.Call();
                    break;
                default:
                    B = false; 
                    break;
            }
            if (B)
            {
                break;
            }
        }
    }
}
