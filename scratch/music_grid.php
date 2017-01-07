<!DOCTYPE html>
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="normalize.css">
    <link rel="stylesheet" type="text/css" href="skeleton.css">

    <link rel="stylesheet" type="text/css" href="schema.css">
    <title>music - mhlinder</title>
  </head>

  <body>

    <div class="main mono container">

      <div class="row space-after">
        <strong><a href="index">back</a></strong>
      </div>

      <div class="row space-after">
        <strong>music</strong> - <a href="#" id="collapse">collapse</a> / <a href="#" id="expand">expand</a>
      </div>

      <div class="row">
        <div class="six columns">

          <ul>
            <li><a href="https://hypem.com/mhlinder">hypem</a></li>
            <li class="space-after"><a href="http://last.fm/user/chimerical_brio">last.fm</a></li>

            <li><?php include('youtube.html')      ?></li>
            <li class="space-after"><?php include('some-songs.html');  ?></li>

            <li><?php include('2016-07--.html');   ?></li>
            <li><?php include('2016-01--06.html'); ?></li>
            <li><?php include('2015-09--12.html'); ?></li>
            <li><?php include('2015-06--08.html'); ?></li>
          </ul>

        </div> <!-- .six.columns -->

        <div class="six columns">

          <ul>
            <li><?php include('2013-03--2015-05.html'); ?></li>
          </ul>

      </div> <!-- .row -->
    </div> <!-- .main .mono .container -->

<script>
    var playlists = ['youtube', 'some-songs', '00-Transition', '01-Brooklyn', '02-rapidfire', '03-springing', '04-rained', '05-mets', '06-forty', '07-jazz', '08-ambient', '09-dsge', '10-metropolish-hastings-linder', '11-yale', '12-late-summer', '13-ability', '14-stated-purpose', '15-accidental-overwrite', '16-omens', '17-conn', '18-18', '19-lame-duck', '20-ocr', '21-vagabond', '22-students-t', '23-apple-pickin', '24-midterms', '25-nets', '26-online-means', '27-thanksiving', '28-finals', '29-felix-navidad', '30-crosscountry', '31-snow', '32-winter-has-come', '33-sprung', '34-indian-winter', '01-orals', '02-new-haven', '03-june', '04-welcome-july', '05-brief', '06-hottern-satans-butthole', '07-ct-to-a2', '08-a2-ct', '09-falling', '10-tim-and-ericnet', '1-shiny', '2-carlos-dangerfield', '3-lofty-heights', '4-probably', '5-earlyfreeze', '6-busy', '7-midterms', '8-crescendo', '9-france', '01-nhalone', '02-jogged', '03-spring-semester', '04-11', '05-glacial', '06-ground-to-a-half', '07-moving', '01-ct', '02-bloom', '03-new-bed', '04-shanghai', '05-salute'];
    for (i = 0; i < playlists.length; i++) {
        var pl_key = playlists[i];
        function toggle_visible(x) {
            var in_key = x.target.id.split('-title')[0],
                key = document.getElementById(in_key.concat('-body'));

            if (key.style.display == 'none') {
                key.style.display = 'block';
            } else {
                key.style.display = 'none';
            }
        }
        document.getElementById(pl_key.concat('-title'))
            .addEventListener('click', function(e) { e.preventDefault(); toggle_visible(e); });
    }
 function collapse() {
     for (i = 0; i < playlists.length; i++) {
         var x = playlists[i];
         key = document.getElementById(x.concat('-body'));
         key.style.display = 'none';
     }
 }
 function expand() {
     for (i = 0; i < playlists.length; i++) {
         var x = playlists[i];
         key = document.getElementById(x.concat('-body'));
         key.style.display = 'block';
     }
 }

  document.getElementById('collapse')
          .addEventListener('click', function(e) { e.preventDefault(); collapse();})
  document.getElementById('expand')
             .addEventListener('click', function(e) { e.preventDefault(); expand();})

</script>


  </body>
</html>

