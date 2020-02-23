using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Light_controller : MonoBehaviour
{
    public Client client;
    public bool Enable;
    public Sprite off;
    public Sprite on;
    public MikuController controller;
    public Image image;
    public void Call()
    {
        if (Enable)
        {
            Enable = false;
            image.sprite = off;
            client.mess = "06|1";
            client.SendMessage();
        }
        else
        {
            Enable = true;
            image.sprite = on;
            client.mess = "06|0";
            client.SendMessage();
        }
    }
}
