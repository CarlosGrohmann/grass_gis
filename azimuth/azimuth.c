#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

/* max vertex per line */
#define MAX_VERTEX 100
/* maxlines per file */
#define MAX_LINHAS 20000
/* PI */
/*#define PI 3.141592654*/

FILE *entrada, *saida;
char arquivo_in[30],arquivo_out[30];
char header_stuff[12],linha[2],layer[1],layer_cat[7],cat[10];
double utm_n[MAX_LINHAS][MAX_VERTEX],utm_e[MAX_LINHAS][MAX_VERTEX]; 
double dx,dy,azim,hyp,arc,m; 
int i,j,k,n_vertex[MAX_LINHAS],n_linhas,n_pontos; 


main()
{
system("clear"); /* clear screen */

/* legal notes...*/	
	
printf("\n**************   AZIMUTH  0.5   **************\n\n");
printf("AZIMUTH calculates azimuth and lengths of vector\n");
printf("lines from DIG_ASCII files exported from GRASS-GIS.\n\n");
printf("Carlos H. Grohmann. IGc-USP-Brasil.  guano@usp.br\n");
printf("Code improvement after suggestions from\n");
printf("Ors Teglasy, Hungary.  orsteglasy@yahoo.com\n");
printf("This program is licenced under GPL 2.0 or later.\n\n");

printf("Your vector file should be exported with v.out.ascii\n");
printf("using the 'standard' format\n");
printf("like this: v.out.ascii input=vector output=ascii format=standard\n");
printf("---------------------------------------------------------\n");
printf("WARNING: version < 6.0 DIG_ASCII files have different format!\n");
printf("Don't use them as input!\n");
printf("WARNING: using -o (old format) option will result in incorrect output!\n");
printf("---------------------------------------------------------\n\n");


/* open input file... */
printf("Input DIG-ASCII file:   ");
scanf("%s",&arquivo_in);
	if(!(entrada=fopen(arquivo_in,"r")))
	{
	printf("\nError opening file!\n");
	exit(1);
	}

/* open output file...*/
printf("\nOutput (Azimuth/Length) file:   ");
scanf("%s",&arquivo_out);
	if((saida=fopen(arquivo_out,"w"))==NULL)
	{
	printf("\nCan't open file!\n");
	exit(1);
	}

/* read dig-ascii file header */
while(!feof(entrada))
	{
	fscanf(entrada,"%s",&header_stuff);
	if(strcmp(header_stuff,"VERTI:")==0) break;
	}
	
/* start line and vertex counters */
j=0; /* line counter */
k=0; /* vertex counter */

while(!feof(entrada))
{ 
   n_linhas=j;
	fscanf(entrada,"%s",&linha);
	fscanf(entrada,"%d",&n_vertex[j]);
	fscanf(entrada,"%d\n",&layer);

/*put the vertex in arrays */
       for(k=0;k<n_vertex[j];k++)
        {
	fscanf(entrada,"%lf",&utm_e[j][k]);
	fscanf(entrada,"%lf",&utm_n[j][k]);
        }
	fscanf(entrada,"%s",&layer_cat);
	fscanf(entrada,"%s",&cat);
j++;

}

printf("\nProcessing...\n");

for (j=0;j<n_linhas;j++)
 {

/* if it is a N-S line */
if(utm_e[j][0]==utm_e[j][n_vertex[j]-1])
	azim=0,
	hyp=abs(utm_n[j][0]-utm_n[j][n_vertex[j]-1]);
	else

		/* if it is a E-W line */
		if(utm_n[j][0]==utm_n[j][n_vertex[j]-1])
		azim=90,
		hyp=abs(utm_e[j][0]-utm_e[j][n_vertex[j]-1]);
		else
			/* if first point of line is to West of second point */
			if(utm_e[j][0]<utm_e[j][n_vertex[j]-1])
			{
			printf("\n linha %d: x0 menor que x1   ", j+1),
				m=(utm_n[j][n_vertex[j]-1]-utm_n[j][0])/(utm_e[j][n_vertex[j]-1]-utm_e[j][0]),
			printf("m= %f   ",m),
				dx=abs(utm_e[j][0]-utm_e[j][n_vertex[j]-1]),
				dy=abs(utm_n[j][0]-utm_n[j][n_vertex[j]-1]),
				hyp=hypot(dx,dy),
				arc=atan(dx/dy),
				azim=(arc*180)/M_PI;
					if(m<0) azim=180-azim;
			printf("azim= %3.2f\n",azim);
			}
				else
					
					/* if first point of line is to East of second point */
					if(utm_e[j][0]>utm_e[j][n_vertex[j]-1])
					{
					printf("\n linha %d: x0 maior que x1   ", j+1),
						m=(utm_n[j][0]-utm_n[j][n_vertex[j]-1])/(utm_e[j][0]-utm_e[j][n_vertex[j]-1]),
					printf("m =%f    ",m),
						dx=abs(utm_e[j][0]-utm_e[j][n_vertex[j]-1]),
						dy=abs(utm_n[j][0]-utm_n[j][n_vertex[j]-1]),
						hyp=hypot(dx,dy),
						arc=atan(dx/dy),
						azim=(arc*180)/M_PI;
						if(m<0) azim=360-azim; else azim=180+azim;
					printf("azim= %3.2f\n",azim);
					}
					
					
					
fprintf(saida,"%3.2f %7.3f\n",azim,hyp);

 }

printf("\n*** Done ***\n");

fclose(entrada);
fclose(saida);

return 0;
}
