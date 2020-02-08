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

public void Active(string[] datapack)
    {
        animator.SetBool("Active", true);

        temp.text = datapack[1]+ "°C";
        hum.text = datapack[2] + "%";
        //Fetch weather data
        switch (datapack[3])
        {
            case "rain":
                image.sprite = spritespack[7];
                break;
            default:

                break;
        }
    }
public void request_data()
    {
        client.mess = "05";
        client.SendMessage();
    }
    public void Off()
    {
        animator.SetBool("Active", false);
        

    }

}
