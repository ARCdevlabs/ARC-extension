using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;

using pyRevitLabs.NLog;

namespace HelloWorld
{
   public class MyCSharpCommand : IExternalCommand
   {
      // define the logger field
      private Logger logger = LogManager.GetCurrentClassLogger();

      public Result Execute(ExternalCommandData revit, ref string message, ElementSet elements)
      {
         // logger.Info("C# test is OK");
         // logger.Debug("Logger works...");
         TaskDialog.Show("Hello Son", "Đây là code được viết bằng C# thông qua pyrevit");
         return Result.Succeeded;
      }
   }
}



