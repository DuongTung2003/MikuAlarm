using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DebugScript : MonoBehaviour
{
    public LookControl control;
    public string data1;
    public string data2;
    public void SendData()
    {
        string[] data = new string[2];
        data[0] = data1;
        data[1] = data2;
        control.moving_target( data);
    }

}
