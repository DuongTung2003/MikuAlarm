using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Text;
public class texthandler : MonoBehaviour
{
    public Text text1;
    public Text text2;
    public string ip;
    public string alarm;
   
    private void Update()
    {
        if (text1)
        {
            byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(text1.text);
            ip = text1.text;//Encoding.ASCII.GetString(clientMessageAsByteArray);

        }
        if (text2)
        {
            
            alarm = text2.text;
            
        }
        
    }

}
