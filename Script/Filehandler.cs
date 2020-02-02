using System.IO;

using UnityEngine;
using UnityEngine.UI;
using TMPro;
public class Filehandler : MonoBehaviour
{

    //private static string path = "Assets/songlist.txt";
    public string data;
    public string[] songlist;
    public GameObject template;
    private Vector3 pos ;
    public Transform list;
    public string sendserver = "04";
    public int[] datatoui = new int[2];
    private int currentsong = 0;
    public Client client;
    public Filehandler filehandler;
    public GameObject close;
    public Material pressedmat;
    public bool isclone;
    // Start is called before the first frame update
    void Start()
    {
        if (!isclone)
        {
            if (close)
            {
                close.SetActive(false);
            }
            //StreamReader reader = new StreamReader(path);
            //data = reader.ReadToEnd();
            string[] song = data.Split('~');
            songlist = new string[song.Length];
            for (int i = 0; i < song.Length - 1; i++)
            {
                string[] name = song[i].Split('|');
                songlist[i] = name[1];


            }
            pos = new Vector3(-20, 331, 0);
            for (int a = 0; a < songlist.Length; a++)
            {
                string namesong = "song" + a.ToString();
                if (GameObject.Find(namesong))
                {
                    Destroy(GameObject.Find(namesong));
                }
                GameObject clone = Instantiate(template, list);
                clone.GetComponent<Transform>().localPosition = pos;
                clone.name = "song" + a.ToString();
                pos += new Vector3(0, -188, 0);
                Transform clonetrans = clone.GetComponent<Transform>();
                Transform transsong = clonetrans.Find("songname");
                Transform transnum = clonetrans.Find("num");
                transsong.GetComponent<Text>().text = songlist[a];
                transnum.GetComponent<TextMeshProUGUI>().text = a.ToString() + "|";
                if (client.rec[1] != "")
                {
                    string recsong = client.rec[1];
                    recsong += "|" + songlist.Length.ToString();
                    string[] reclist = recsong.Split('|');
                    for (int i = 0; i < reclist.Length; i++)
                    {
                        if (a.ToString() == reclist[i])
                        {
                            if (!sendserver.Contains("|" + a.ToString()))
                            {
                                Debug.Log("Playlist: " + a);
                                sendserver += "|" + a.ToString();
                                clone.GetComponent<Image>().material = pressedmat;
                                clonetrans.Find("num").GetComponent<TextMeshProUGUI>().text = i.ToString() + "|";
                            }

                        }
                    }
                }
            }
     
        }

     
        for (int i = 0; i < 100; i++)
        {
            if (close)
            {
                close.SetActive(false);
            }
        }
        

    }
        
    public  void sendreset(bool reset)
    { if (reset == true)
        {
            filehandler.sendserver = "04";
            filehandler.currentsong = 0;
            client.rec[1] = "";
            filehandler.Start();
        }
        else
        {
            Debug.Log("Trying to send: " + sendserver);
            client.mess = sendserver;
            client.SendMessage();
        }
    }
    
    public int[] register(bool reset,int num)
        {
        int code = 0;
        switch (reset)
        {
            case false:
                if (sendserver.Contains("|"+num.ToString()))
                {
                    //delete
                    sendserver = sendserver.Replace("|"+num.ToString(),"");
                    code = 1;
                    currentsong -= 1;
                }
                else
                {
                    sendserver += "|"  + num.ToString();
                    code = 2;
                    currentsong += 1;
                }

                break;
            case true:
                sendserver = "04";
                currentsong = 0;
                Start();
                code = 3;
               
                break;
        }
        
        datatoui[0] = code;
        datatoui[1] = currentsong;
        Debug.Log("Data: " + datatoui[0] + "   " + datatoui[1]);
        return datatoui;
    }



    

    // Update is called once per frame

}
