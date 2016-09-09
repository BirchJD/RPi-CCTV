<?php

// RPiCCTV - CCTV System for Raspberry Pi
// Copyright (C) 2016 Jason Birch
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see &lt;http://www.gnu.org/licenses/>.

/**************************************************************************/
/* V1.00   2016-09-02  Jason Birch                                        */
/*                                                                        */
/* Web page to get a recent image from the recording video. To display in */
/* a summary web page.                                                    */
/**************************************************************************/

   system("/usr/lib/cgi-bin/wwwFrame.sh");

   $Filename = "/var/www/html/image.jpg";
   if (($File = fopen($Filename, "r")))
   {
      $Image = fread($File, filesize($Filename));
      fclose($File);
      
      header('Content-Type: image/jpeg');
      header('Content-Length: ' . filesize($Filename));
      print($Image);
   }
?>

