using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Animationtrigger : MonoBehaviour
{
    public Animator animator;
    public string animation1;
    public string StopAnimation1;
    public string StartAnimation1;
    public bool opening;
    public int StartValue;
    public int EndValue;
    public int Value;
    public void Animation1()
    {
        if (Value < EndValue)
        {
            Value += 1;

        }
        else
        {
            Value = StartValue;
        }
        animator.SetInteger(animation1, Value);
    }
    public void event1()
    {
        if (opening == false)
        { animator.SetFloat(StopAnimation1, 0f); }
        else { animator.SetFloat(StartAnimation1, 1f); }
        opening = !opening;
    }


}
