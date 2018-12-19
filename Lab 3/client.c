#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
 
int main(int argc, char * argv[])
{
  int sockfd = 0,n = 0;
  char recvBuff[1024];
  struct sockaddr_in serv_addr;
 
  if(argc < 2)
    {
      printf("\n Error : Host name and message not given \n");
      return 1;
    }
  else if(argc < 3)
    {
      printf("\n Error : Message not given");
      return 1;
    }

  memset(recvBuff, '0' ,sizeof(recvBuff));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }

  struct hostent *host = gethostbyname(argv[1]);
  if(host == NULL)
    {
      printf("\n Error : Host not found \n");
      return 1;
    }
  
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(5000);

  bcopy((char *)host->h_addr,(char *)&serv_addr.sin_addr.s_addr, host->h_length);
 
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
  printf("\n Sending Message : %s", argv[2]);
  send(sockfd, argv[2], strlen(argv[2]), 0);
  printf("\n Message Sent \n");
  int i = 0;
  while(i < 1024)
    {
      recvBuff[i] = '\0';
      i++;
    }
  while((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0)
    {
      recvBuff[n] = 0;
      if(fputs(recvBuff, stdout) == EOF)
        {
          printf("\n Error : Fputs error");
        }
      printf("%s\n", recvBuff);
    }
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
 
  return 0;
}
