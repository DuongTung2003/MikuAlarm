using UnityEngine;

public class MikuController : MonoBehaviour
{
    public Animator animator;
    public int state_ID;
    private float startTime;
    public bool interacted;
    public AudioSource hellowav;
    public AudioSource nicetomeetuwav;
    public float delaytime;
    private float refreshtime;
    public float refreshtimecount;
    public bool looking;
    public LookControl lookControl;
    public Client client;
    void Start()
    {   
        startTime = Time.time;
        startanim();

    }
 
    public void startanim()
    {
       
        state_ID = Random.Range(0, 2);
        Debug.Log("Random ID:" + state_ID);
        animator.SetInteger("State_ID", state_ID);
        switch (state_ID)
        {
            case 0:
                hellowav.Play();
                break;
            case 1:
                nicetomeetuwav.Play();
                break;
            default:
                break;
        }
    }
    void Update()
    {
        try
        {
            looking = client.looking;
        }
        catch (System.Exception)
        {
            Debug.LogError("Fetch client position data failed");
            throw;
        }
       
        if (!animator.GetCurrentAnimatorStateInfo(0).IsName("hello") && !animator.GetCurrentAnimatorStateInfo(0).IsName("nicetomeetyou") && !animator.GetCurrentAnimatorStateInfo(0).IsName("New State") )
        {
            if (refreshtimecount + refreshtime < Time.time)
            {


                refreshtime = Time.time;
                Debug.Log("Idle mode");
                Debug.Log("Time: " + (Time.time - startTime).ToString());
                if (startTime + delaytime < Time.time && looking == false)
                {
                    startTime = Time.time;
                    state_ID = 4;
                    animator.SetInteger("State_ID", state_ID);

                    interacted = false;
                }
                else if (interacted && looking == false)
                {

                    state_ID = Random.Range(2, 4);

                    animator.SetInteger("State_ID", state_ID);
                }
                else if (looking)
                {
                    state_ID = 5;
                    animator.SetInteger("State_ID", state_ID);
                }
                Debug.Log("State " + state_ID);
            }
        }
    }
}
