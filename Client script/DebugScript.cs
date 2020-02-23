using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DebugScript : MonoBehaviour
{
    public LookControl control;
    public string data1;
    public string data2;
    public bool random;
    public void SendData()
    {
        if (random)
        {
            data1 = Random.Range(0, 100).ToString();
            data2 = Random.Range(0, 100).ToString();
        }
        string[] data = new string[3];
        data[1] = data1;
        data[2] = data2;
        control.moving_target( data);
    }

}
