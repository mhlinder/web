
<!DOCTYPE html>
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="schema.css?b=1">
    <title>music - mhlinder</title>
  </head>

  <body>

    <div class="main mono">
      <p>
        <h1 class="left"><a href="index">music</a></h1>
        <ul>
          <li><a href="https://hypem.com/mhlinder">hypem</a></li>
          <li><a href="http://last.fm/user/chimerical_brio">last.fm</a></li>
        </ul>
      </p>

      <p>
        <ul>
          <li>playlists
            <ul>
              <li><div id="youtube">
                <strong><a href="#" id="youtube-title">youtube</a></strong>
                <div id="youtube-body" style="display: none;">
                  <ul class="space-before space-after">
                    <?php include('youtube.html'); ?>
                  </ul>
                </div>
              </div>
              </li>
              <li>
                <div id="some-song">
                  <strong><a href="#" id="some-songs-title">some songs</a></strong>
                  <div id="some-songs-body" style="display: none;">
                    <p class="space-before space-after">
                    I listened to a lot of punk when I was growing up, and something I've
                    really dug in the aughts has been the ascendency of
                    <a href="https://www.youtube.com/watch?v=fHYea2R55TQ"
                       target="_blank">lofi</a>-<a href="https://www.youtube.com/watch?v=KAg4kN5pi3U"
                        target="_blank">garage</a>-<a href="https://www.youtube.com/watch?v=G_O5TQVdono"
                        target="_blank">psychadelic</a>-<a href="https://www.youtube.com/watch?v=h7GZLRxVzvg"
                        target="_blank">noise</a>-<a href="https://www.youtube.com/watch?v=mmDVrZKnk_k"
                        target="_blank">blues</a>
                    rock...I mean music for eg
                    <a href="https://www.youtube.com/watch?v=TigJYxitYLg"
                       target="_blank">slackers</a>
                    or <a href="https://www.youtube.com/watch?v=JKsvBFiA1WQ"
                          target="_blank">surf bums</a>
                    or <a href="https://www.youtube.com/watch?v=0H2wvspO29c"
                          target="_blank">loud punks</a>
                    or <a href="https://www.youtube.com/watch?v=ZdRBAdzNhsw"
                          target="_blank">gross punks</a>
                    or <a href="https://www.youtube.com/watch?v=040wZ3p5wRk"
                          target="_blank">nympho punks</a>
                    or <a href="https://www.youtube.com/watch?v=sAkW1wXGlU0"
                          target="_blank">disaffected punks</a>.
                    </p>
                  </div>
                </div>
              </li>

              <?php include('playlists.html'); ?>
            </ul>
          </li>
      </p>
    </div>

  </body>

</html>

