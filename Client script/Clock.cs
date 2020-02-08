using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using TMPro;


public class Clock : MonoBehaviour
{
    public TextMeshProUGUI time;
    public TextMeshProUGUI date;
    void Update()
    {
        time.text = System.DateTime.Now.ToString("h:mm:ss tt");
        date.text = System.DateTime.Now.ToString("D", System.Globalization.CultureInfo.CreateSpecificCulture("en-US"));
    }
}
