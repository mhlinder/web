
<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" type="text/css" href="schema.css">
  <title>music - mhlinder</title>
</head>

<body>

<div class="main mono">
  <p>
    <h1 class="left"><a href="index">music</a></h1>
  <ul>
    <li><a href="https://hypem.com/mhlinder">hypem</a>
    <li><a href="http://last.fm/user/chimerical_brio">last.fm</a>
  </ul>
  </p>

  <p>
  <ul>
    <li><strong>playlists</strong>
      <ul>
        <li><div id="youtube">
          <strong><a href="#" id="youtube-title">youtube</a></strong>
            <div id="youtube-body" style="display: none;">
              <ul class="space-after">
                <?php include('youtube.html'); ?>
              </ul>
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

