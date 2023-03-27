<h1>Movies</h1>
<!-- MOVIES -->
<div class="d-flex flex-wrap">
<?php
    require_once('functions.php');
    $movies = getMovies(0, 50);
    foreach ($movies as $movie) {
        ?>
            <div class="card m-3">
                <a href="/movie?id=<?php echo $movie["id"] ?>" class="link"></a>
                <div class="card-header">
                    <h4 class="card-title">
                        <?php echo $movie["title"] ?>
                    </h4>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        <?php echo $movie["genres"] ?>
                    </p>
                </div>
                <div class="card-footer text-muted">
                    
                </div>
            </div>
        <?php
    }
?>
</div>