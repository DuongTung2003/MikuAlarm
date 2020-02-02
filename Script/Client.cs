//using System;
//using System.Net.Sockets;
//using System.Text;
//using UnityEngine;
//using UnityEngine.UI;
//using TMPro;
//public class Client : MonoBehaviour
//{
//    private const int portNum = 3939;
//    private string hostName = "192.168.0.106";
//    public TMP_Text StatusText;
//    public string alarmset = "06:00";
//    public bool setalarm = false;
//    //private const string hostName = "127.0.1.1";
//    public Text ip;
//    public void startconnect()
//    {
//        if (ip.text != null || ip.text != "")
//        {
//            hostName = ip.text;
//        }
//        try
//        {   
//            var client = new TcpClient(hostName, portNum);
//            StatusText.text = "Server Online";
//            StatusText.color = new Color(0, 255, 0);

//            NetworkStream ns = client.GetStream();


//               byte[] bytes = new byte[1024];
//               int bytesRead = ns.Read(bytes, 0, bytes.Length);
//               string alarm = Encoding.ASCII.GetString(bytes, 0, bytesRead);
//            while (setalarm == false)
//                   {

//                   }
//            byte[] bytesent = new byte[1024];
//            bytesent =  System.Text.Encoding.ASCII.GetBytes(alarmset);
//            ns.Write(bytesent,0,bytesent.Length);
//            Debug.Log(alarm);
//            ns.Close();
//            client.Close();



//        }
//        catch (Exception e)
//        {
//            StatusText.text = "Connect failed";
//            StatusText.color = new Color(255, 0, 0);
//            Debug.LogError(e.ToString());
//        }


//    }
//}
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Client : MonoBehaviour
{
    #region Variable	
    private TcpClient socketConnection;
    private Thread clientReceiveThread;
    private const int portNum = 3939;
    public string hostName;
    public TMP_Text StatusText;
    public string alarmset = "06:00";
    public bool setalarm = false;
    //private const string hostName = "127.0.1.1";
    public string[] rec;
    public texthandler ip;
    public string mess;
    private bool connection;
    private float currenttime = 0;
    private bool starttimer;
    public GameObject open;
    public GameObject close;
    public Transform move;
    public string[] iplist = new string[5];
    private int count;
    public string[] songlist = new string[57];
    public bool connected;
    private int index = 0;
    public float[] lookposition = new float[2];
    public bool looking;
    public LookControl lookControl;
    #endregion
    // Use this for initialization 	
    public void Start()
    {
        if (connected == false)
        {

            if (ip.ip != "")
            {
                Debug.Log("<" + ip.ip + "/>");
                hostName = ip.ip;
            }

            ConnectToTcpServer();
        }
    }
    // Update is called once per frame



    /// <summary> 	
    /// Setup socket connection. 	
    /// </summary> 	
    private void Update()
    {
        if (connection == true)
        {
            StatusText.text = "Server Online";
            StatusText.color = new Color(0, 255, 0);
            if (starttimer == false)
            {
                starttimer = true;
                currenttime = Time.time;
            }
            
            if (Time.time >= currenttime + 2)
            {
                open.SetActive(true);
                close.SetActive(false);
                move.position += new Vector3(0,5000, 0);
            }
        }
        else
        {
            StatusText.text = "Server Offline";
            StatusText.color = new Color(255, 0, 0);
        }
    }
    private void ConnectToTcpServer()
    {
        try
        {
            clientReceiveThread = new Thread(new ThreadStart(ListenForData));
            clientReceiveThread.IsBackground = true;
            clientReceiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.Log("On client connect exception " + e);
        }
    }
    /// <summary> 	
    /// Runs in background clientReceiveThread; Listens for incomming data. 	
    /// </summary>     
    private void ListenForData()
    {
        if (connected == false)
        {


            Debug.Log(hostName + ":" + portNum.ToString());
            try
            {
                socketConnection = new TcpClient(hostName, portNum);
                connection = true;
                connected = true;
                Byte[] bytes = new Byte[1024];
                while (true)
                {
                    // Get a stream object for reading 				
                    using (NetworkStream stream = socketConnection.GetStream())
                    {
                        int length;
                        // Read incomming stream into byte arrary. 					
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            var incommingData = new byte[length];
                            Array.Copy(bytes, 0, incommingData, 0, length);
                            // Convert byte array to string message. 						
                            string serverMessage = Encoding.ASCII.GetString(incommingData);
                            Debug.Log("server message received as: " + serverMessage);
                            string[] param = serverMessage.Split(' ');
                            switch (param[0])
                                { 
                                 case "05":
                                    lookControl.moving_target(param);
                                    break;
                                
                                 default:
                                     rec[index] = serverMessage;
                                     index += 1;
                                     break;
                        }
                        }
                    }
                }
            }
            catch (SocketException socketException)
            {
                connection = false;
                Debug.Log("Socket exception: " + socketException);
                if (count < iplist.Length)
                {
                    hostName = iplist[count];
                    count += 1;
                }


                Start();
                return;
            }
        }
    }
    /// <summary> 	
    /// Send message to server using socket connection. 	
    /// </summary> 	
    public void SendMessage()
    {
        if (socketConnection == null)
        {
            return;
        }
        try
        {
            // Get a stream object for writing. 			
            NetworkStream stream = socketConnection.GetStream();
            if (stream.CanWrite)
            {
                
                // Convert string message to byte array.                 
                byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(mess);
                // Write byte array to socketConnection stream.                 
                stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
                Debug.Log("Client sent his message - should be received by server");
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }
}