using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.UI;
using TMPro;

public class songpress : MonoBehaviour
{
    public Filehandler handler;
    public Material pressedmat;
    public Material newmat;
    public void pressed()
    {


        
        string parenttrans = gameObject.GetComponentInParent<Transform>().name;
        parenttrans.Replace("song", "");
        string text = transform.Find("num").GetComponent<TextMeshProUGUI>().text;
        string[] textlist = text.Split('|');
        Debug.Log("~" + textlist[0] + "~");
        int sendcode = int.Parse(textlist[0]);
        int tosend = int.Parse(gameObject.name.Replace("song", ""));
        Debug.Log("sendcode: " + sendcode);
        int[] code = handler.register(false,tosend);
        Debug.Log("code 0 :"+code[0]);
        Debug.Log("code 1 :"+code[1]);
        switch (code[0])
        {
            case 1:
                //gameObject.GetComponent<Image>().color = new Color(255, 255, 255);
                GetComponent<Image>().material = newmat;
                transform.Find("num").GetComponent<TextMeshProUGUI>().text = tosend.ToString() + "|";
                break;
            case 2:
                //gameObject.GetComponent<Image>().color = new Color(126,255,230);
                GetComponent<Image>().material = pressedmat;
                transform.Find("num").GetComponent<TextMeshProUGUI>().text = code[1].ToString() + "|";
                break;
        }
        
    }
}
