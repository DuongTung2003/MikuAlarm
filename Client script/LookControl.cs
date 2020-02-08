
using UnityEngine;
using Live2D.Cubism.Core;
using Live2D.Cubism.Framework;
public class LookControl : MonoBehaviour
{
    // [-3,3]       [3,3]
    // [-3,-5]      [3,-5]

    public MikuController controller;
    public Client client;
    public Transform target;
    public float time;
    public Animator animator;
    private float angleX;
    private float angleY;
    private float bgX;
    private float bgY;
    private float[] posbg = new float[2];
    static float t = 0.0f;
    public bool moving;
    public string[] recpos = new string[2];
    public float SpaceX;
    public float SpaceY;
    public float Speed;
    private float tarX;
    private float tarY;
    public void moving_target(string[] data)
    {
        Debug.Log("X " + data[0]);
        Debug.Log("Y " + data[1]);
        recpos = data;

        moving = true;

        
    }
    public void OnActive(bool State)
    {
        if (State)
        {
            client.mess = "02|01";
            client.SendMessage();
        }
        else
        {
            client.mess = "02|02";
            client.SendMessage();
        }
        Debug.Log("Sent camera state "+ State);
    }
    

    private void FixedUpdate()
    {

        if (recpos[0] != "")
        {
            tarX = (float.Parse(recpos[0]) / 100) * 6 - 3;
            tarY = (float.Parse(recpos[1]) / 100) * 8 - 5;
            target.position = Vector3.Lerp(target.position, new Vector3(tarX, tarY, 0), Time.deltaTime * Speed);
        }

        #region comment
        //if (targetmoving)
        //{
        //    float tarX = (float.Parse(recpos[0]) / 100) * 8 - 5;
        //    float tarY = (float.Parse(recpos[1]) / 100) * 6 - 3;
        //    if (Mathf.Abs(target.position.x) - Mathf.Abs(tarX) < SpaceX + 0.05f)
        //    {
        //        target.position = new Vector3(tarX, target.position.y, target.position.z);
        //        targetmoving = false;
        //    }
        //    if (Mathf.Abs(target.position.y) - Mathf.Abs(tarY) < SpaceY + 0.05f)
        //    {
        //        target.position = new Vector3(target.position.x, tarY, target.position.z);
        //        targetmoving = false;
        //    }
        //    if (target.position.x != tarX)
        //    {

        //        if (target.position.x > tarX)
        //        {
        //            target.position = new Vector3(target.position.x - SpaceX, target.position.y, target.position.z);
        //        }
        //        else if (target.position.x < tarX)
        //        {
        //            target.position = new Vector3(target.position.x + SpaceX, target.position.y, target.position.z);
        //        }


        //    }
        //    if (target.position.y != tarY)
        //    {

        //        if (target.position.y > tarY)
        //        {
        //            target.position = new Vector3(target.position.x, target.position.y - SpaceY, target.position.z);
        //        }
        //        else if (target.position.y < tarY)
        //        {
        //            target.position = new Vector3(target.position.x, target.position.y + SpaceY, target.position.z);
        //        }


        //    }
        //    Debug.Log("Moving");


        // }
        #endregion
        //Debug.Log("Time: " + time.ToString());
        if (moving == false)
        {
            bgX = animator.GetFloat("LookPosHoz");
            bgY = animator.GetFloat("LookPosVer");
            t = 0.0f;
            if (posbg[0] != target.position.x || posbg[1] != target.position.y)
            {
                moving = true;
                posbg[0] = target.position.x;
                posbg[1] = target.position.y;
            }
            
            
        }
        else
        {
           

            controller.interacted = true;
            float targetX = target.position.x;
            float targetY = target.position.y;
            float eyeX = Mathf.Lerp(bgX, (((targetX + 4.3f) / 3) - 1f), t);
            float eyeY = Mathf.Lerp(bgY, (((targetY + 5.3f) / 4) - 1f), t);
            angleX = Mathf.Lerp(bgX, (((targetX + 2) / 3) - 1f), t);
            angleY = Mathf.Lerp(bgY, (((targetY + 4) / 4)-1f), t);
            Debug.Log("target: X " + targetX.ToString() + " Y: " + targetY.ToString());
            t += 0.5f * Time.deltaTime;
            animator.SetFloat("LookPosHoz", angleX);
            animator.SetFloat("LookPosVer", angleY);
            animator.SetFloat("EyeballX", eyeX);
            animator.SetFloat("EyeballY", eyeY);
        }
    }


}
