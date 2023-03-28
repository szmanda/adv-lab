<h1>Movies</h1>
<!-- MOVIES -->
<a href="movie_add.php">Add movie</a>
<!-- Buttons for handling pagination -->
<?php
    $page = 0;
    if (isset($_GET['page']))
        $page = $_GET['page'];
?>
<div class="d-flex justify-content-left">
    <a href="?page=0" class="btn btn-outline-secondary m-3">First</a>
    <?php if ($page > 0) { ?>
        <a href="?page=<?php echo $page - 1 ?>" class="btn btn-outline-secondary m-3">Previous</a>
    <?php }?>
    <a href="?page=<?php echo $page + 1 ?>" class="btn btn-outline-secondary m-3">Next</a>
</div>
<div class="d-flex flex-wrap">
<?php
    require_once('functions.php');
    $pageCount = 50;
    $movies = getMovies($page * $pageCount, $pageCount);
    foreach ($movies as $movie) {
        ?>
            <div class="card m-3">
                <a href="/movie.php?id=<?php echo $movie["id"] ?>" class="link"></a>
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