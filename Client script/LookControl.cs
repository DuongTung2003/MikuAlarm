
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
    private float reset_time;



    public void moving_target(string[] data)
    {
        Debug.Log("X " + data[1]);
        Debug.Log("Y " + data[2]);


    }



    private void Update()
    {
        Debug.Log("Time: " + time.ToString());
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
