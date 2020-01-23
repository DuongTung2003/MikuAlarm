using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class setalarm : MonoBehaviour
{
    public Client client;
    public texthandler input;
    public GameObject confirm;
    public TMP_Text old;
    public GameObject close;
    public void Start()
    {
        if (close)
        {
            close.SetActive(false);
        }
        old.text = "Current: " + client.rec[0];
        for (int i = 0; i < 100; i++)
        {
            if (close)
            {
                close.SetActive(false);
            }
        }
    }
    public void set()
    {
        client.mess = "03|"+input.alarm;
        client.SendMessage();
        confirm.SetActive(true);
    }
}
