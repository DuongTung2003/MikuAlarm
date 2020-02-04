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
    public bool Self;
    public Client client;
    public bool onopen;

    
    public void change()
    {
        if (open)
        {
            open.SetActive(true);
        }

        if (open2)
        {
            open2.SetActive(true);
        }
        if (close)
        {
            close.SetActive(false);
        }
        if (close2)
        {
            close2.SetActive(false);
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
