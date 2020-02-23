using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;
public class Weather_control : MonoBehaviour
{
    public Animator animator;
    public TextMeshProUGUI temp;
    public TextMeshProUGUI hum;
    public string data;
    public Sprite[] spritespack = new Sprite[18];
    public Image image;
    public Client client;
    public Toggle toggle;
public void Active(string[] datapack)
    {
        animator.SetBool("Active", true);

        temp.text = datapack[1]+ "°C";
        hum.text = datapack[2] + "%";
        //Fetch weather data
        switch (datapack[3].ToLower())
        {
            case "rain":
                image.sprite = spritespack[7];
                break;
            case "clouds":
                image.sprite = spritespack[0];
                break;
            default:

                break;
        }
    }
public void request_data()
    {
        
        if (toggle.isOn)
        {
            client.mess = "05|1";

        }
        else
        {
            client.mess = "05|0";
        }
        client.SendMessage();
    }
    public void Off()
    {
        animator.SetBool("Active", false);
        

    }

}
