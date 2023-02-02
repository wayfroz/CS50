#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //finding each pixel
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
        {
            //find the average
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            //convert the pixel to the average of each color
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }

    return;
}

int limit(RGB)
{
    if (RGB > 255)
    {
        RGB = 255;
    }
    return RGB;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //finding a pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepia_red = limit(round(image[i][j].rgbtRed * 0.393 + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue));
            int sepia_green = limit(round(image[i][j].rgbtRed * 0.349 + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue));
            int sepia_blue = limit(round(image[i][j].rgbtRed * 0.272 + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue));

            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //finding a pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            int k = width - j - 1;

            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;

            image[i][j].rgbtRed = image[i][k].rgbtRed;
            image[i][j].rgbtBlue = image[i][k].rgbtBlue;
            image[i][j].rgbtGreen = image[i][k].rgbtGreen;

            image[i][k].rgbtRed = red;
            image[i][k].rgbtBlue = blue;
            image[i][k].rgbtGreen = green;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE copy[height][width];

    //declarting forpixels around
    int i, j, k, l;

    //get the value of pixels around
    for (i = 0; i < height; i ++)
    {
        for (j = 0; j < width; j ++)
        {
            //declaring variables
            int total_red = 0;
            int total_green = 0;
            int total_blue = 0;
            float count = 0.0;

            //vertical shift
            for (k = -1; k < 2; k++)
            {
                //horizontal shift
                for (l = -1; l < 2; l++)
                {
                    if (i + k < 0 || i + k > height - 1 || j + l < 0 || j + l > width - 1)
                    {
                        continue;
                    }

                    total_red += image[k + i][l + j].rgbtRed;
                    total_blue += image[k + i][l + j].rgbtBlue;
                    total_green += image[k + i][l + j].rgbtGreen;

                    count++;
                }
            }

            copy[i][j].rgbtRed = round(total_red / count);
            copy[i][j].rgbtBlue = round(total_blue / count);
            copy[i][j].rgbtGreen = round(total_green / count);
        }
    }

    //sub back
    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width; j ++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }
    return;
}
