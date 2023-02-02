#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// lengt of the card number and the order of digits || Declaring
int count = 0;
int sum = 0;
int digit = 0;
int two_digits;
long power;
long cc;

int main(void)
{
    cc = get_long("Enter the cc number: ");
    // store a value in the other variable not to lose it after a while loop
    long card = cc;

    // get every second digit
    while (card > 0)
    {
        //set it to get over every int
        count ++;

        if (count % 2 == 0)
        {
            // get the last secod digit;
            digit = (int)(card % 10);
            digit *= 2;
            if (digit > 9)
                // to get the last digit of the digit with two numbers
            {
                int digit_1 = digit % 10;
                // get the first digit of 2 digits number
                int digit_2 = digit / 10;
                digit = digit_1 + digit_2;
            }
        }
        else if (count % 2 == 1)
        {
            // get the last secod digit;
            digit = (int)(card % 10);
            digit *= 1;
        }
        sum += digit;
        //get rid of the last digit
        card /= 10;
        // getting these digits together in the sum
    }
    if (sum % 10 == 0)
    {
        // depending on the numbers of digits of the cc
        if (count == 13)
        {
            //how much to count from left
            count -= 1;
            // to raise 10 to the power of the digit
            power = pow(10, count);
            two_digits = cc / power;
            if (two_digits == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (count == 15)
        {
            count -= 2;
            power = pow(10, count);
            two_digits = cc / power;
            if (two_digits == 34 || two_digits == 37)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (count == 16)
        {
            count -= 2;
            power = pow(10, count);
            two_digits = cc / power;
            if (two_digits == 51 || two_digits == 52 || two_digits == 53 || two_digits == 54 || two_digits == 55)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                // ad 10 to the power because only one digit matters for VISA
                power = 10;
                two_digits /= power;
                if (two_digits == 4)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}