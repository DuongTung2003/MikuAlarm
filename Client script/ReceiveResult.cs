using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ReceiveResult : MonoBehaviour {

	// Use this for initialization
	void Start () {
        //GameObject.Find("Text").GetComponent<Text>().text = "You need to be connected to Internet";
	}
	
    void onActivityResult(string recognizedText){
        char[] delimiterChars = {'~'};
        string[] result = recognizedText.Split(delimiterChars);

        //You can get the number of results with result.Length
        //And access a particular result with result[i] where i is an int
        //I have just assigned the best result to UI text
        GameObject.Find("Text_test").GetComponent<TextMeshProUGUI>().text = result[0];

    }


}
