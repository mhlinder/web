<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" type="text/css" href="schema.css">
  <title>resume - mhlinder</title>
</head>

<body>

<div class="main mono">
    [<a href="index">M. HENRY LINDER</a>]
    <br />
    <br />

    [<a href="https://twitter.com/mhlinder">
      <?php
      $tomorrow = new DateTime('tomorrow');
      echo strtoupper($tomorrow->format('d M y'));
      ?></a>]

    <br />
    <br />

    [25 AUG 14 -<br />
    &nbsp;<?php echo strtoupper(date('d M y')); ?>&nbsp;UCONN]
      

    <br />
    <br />

    [19 MAY 14 -
        <br />
        &nbsp;15 AUG 14&nbsp;&nbsp;&nbsp;<a href="http://o-c-r.org/">OCR</a>]

    <br />
    <br />

    [22 JUN 12 -<br />
     &nbsp;16 MAY 14 FRBNY]

    <br />
    <br />

    [27 MAY 12
    <br />
    &nbsp;SWARTHMORE COL.]

    <br />
    <br />

    [15 AUG 90]

</div>

</body>

</html>