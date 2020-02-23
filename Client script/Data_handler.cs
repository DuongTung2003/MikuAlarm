using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Data_handler : MonoBehaviour
{
    public Client client;
    public LookControl lookControl;
    public Weather_control Weathercontrol;
    void Update()
    {
        string serverMessage = client.rec;
        string[] param = serverMessage.Split('|');
        switch (param[0])
        {
            case "02":
                lookControl.moving_target(param);
                client.looking = true;
                break;
            case "05":
                Weathercontrol.Active(param);
                break;
            default:
                Debug.Log("Unknow data type");
                break;
        }
        client.rec = "";
    }
}

