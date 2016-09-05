<!--
# RPiCCTV - CCTV System for Raspberry Pi
# Copyright (C) 2016 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/>.

/**************************************************************************/
/* V1.00   2016-09-02  Jason Birch                                        */
/*                                                                        */
/* Web page to get a recent image from the recording video and recent log */
/* entries. Then allow the user to view them.                             */
/**************************************************************************/
-->

<HTML>
   <HEAD>
      <TITLE>RPi CCTV</TITLE>
      <SCRIPT LANGUAGE='JavaScript'>
      <!--
         var Ajax = new XMLHttpRequest();

         function AjaxInclude(ObjectName, Filename)
         {
            Ajax.open("GET", Filename, false);
            Ajax.send();
            document.getElementById(ObjectName).innerHTML = Ajax.responseText;
         }
      -->
      </SCRIPT>
   </HEAD>
   <BODY BGCOLOR='#000000'>
<?php
   system("/usr/lib/cgi-bin/wwwFrame.sh");
?>
      <CENTER>
         <FORM METHOD='POST'>
            <TABLE WIDTH='800'>
               <TR>
                  <TD>
                     <INPUT TYPE='SUBMIT' STYLE='WIDTH: 100%; FONT-WEIGHT: BOLD;' VALUE='REFRESH'><BR>
                  </TD>
               </TR>
               <TR>
                  <TD>
                     <PRE><DIV ID='LogFile' STYLE='COLOR: #000000; BACKGROUND-COLOR: #FFFFFF; WIDTH: 100%; HEIGHT: 200; OVERFLOW: SCROLL;'></DIV></PRE>
                     <SCRIPT LANGUAGE='JavaScript'>
                        AjaxInclude("LogFile", "/log.inc");
                        var LogFile = document.getElementById("LogFile");
                        LogFile.scrollTop = LogFile.scrollHeight;
                     </SCRIPT>
                  </TD>
               </TR>
               <TR>
                  <TD>
                     <IMG SRC='image.jpg'>
                  </TD>
               </TR>
            </TABLE>
         </FORM>
      </CENTER>
   </BODY>
</HTML>

