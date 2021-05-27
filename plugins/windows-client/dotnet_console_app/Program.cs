using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Topshelf;

namespace WindowsSocketClient
{
    class Program
    {
        static void Main(string[] args)
        {

            var exitCode = HostFactory.Run(x =>
            {
                x.Service<Websocket>(s =>
                {
                    s.ConstructUsing(websocket => new Websocket());
                    s.WhenStarted(websocket => websocket.Start());
                    s.WhenStopped(websocket => websocket.Stop());
                });
                
                x.RunAsPrompt();

                x.SetServiceName("Asset Monitoring");
                x.SetDisplayName("Asset Monitoring");
                x.SetDescription("This is connecting this PC to Server");
            });

            int exitCodeValue = (int)Convert.ChangeType(exitCode, exitCode.GetTypeCode());
            Environment.ExitCode = exitCodeValue;
        }
    }
}