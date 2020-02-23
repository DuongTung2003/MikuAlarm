using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class uichange : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject open;
    public GameObject open2;
    public GameObject close;
    public GameObject close2;
    public GameObject open3;
    public bool Self;
    public Client client;
    public bool onopen;
    public bool onStart;
    private void Start()
    {
        if (onStart)
        {

            change();
        }
    }
    public void change()
    {
        if (open)
        {
            open.GetComponent<CanvasGroup>().alpha = 1f;
            open.GetComponent<CanvasGroup>().interactable = true;
            open.GetComponent<CanvasGroup>().blocksRaycasts = true;
        }

        if (open2)
        {
            open2.GetComponent<CanvasGroup>().alpha = 1f;
            open2.GetComponent<CanvasGroup>().interactable = true;
            open2.GetComponent<CanvasGroup>().blocksRaycasts = true;
        }
        if (close)
        {
            close.GetComponent<CanvasGroup>().alpha = 0f;
            close.GetComponent<CanvasGroup>().interactable = false;
            close.GetComponent<CanvasGroup>().blocksRaycasts = false;
        }
        if (close2)
        {
            close2.GetComponent<CanvasGroup>().alpha = 0f;
            close2.GetComponent<CanvasGroup>().interactable = false;
            close2.GetComponent<CanvasGroup>().blocksRaycasts = false;
        }
        if (open3)
        {
            open3.SetActive(true);
        }
        if (Self)
        {
            gameObject.SetActive(false);
        }

    }
    public void connect(bool Exit)
    {
        if (Exit)
        {
            client.Start();
        }
        else
        {
            client.mess = "00";
            client.SendMessage();
            Application.Quit();
        }
        
    }
    public void slider()
    {
        int list = GameObject.Find("confirm").GetComponent<Filehandler>().songlist.Length;
        Transform transform = open.GetComponent<Transform>();
        Scrollbar scrollbar = gameObject.GetComponent<Scrollbar>();
        float val = scrollbar.value;
        float calculated = val *((list * 188));
        transform.localPosition = new Vector3(0, calculated, 0);
        
        
    }
}
