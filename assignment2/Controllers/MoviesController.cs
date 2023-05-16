using Microsoft.AspNetCore.Mvc;
namespace web_services_l1.Controllers;
[ApiController]
[Route("[controller]")]
public class MoviesController : ControllerBase
{
    [HttpPost("UploadMovieCsv")]
    public string Post(IFormFile inputFile)
    {
        var strm = inputFile.OpenReadStream();
        byte[] buffer = new byte[inputFile.Length];
        strm.Read(buffer, 0, (int)inputFile.Length);
        string fileContent = System.Text.Encoding.Default.GetString(buffer);
        strm.Close();

        MoviesContext dbContext = new MoviesContext();

        bool skip_header = true;
        List<Genre> genres = new List<Genre>();
        List<Movie> movies = new List<Movie>();
        foreach(string line in fileContent.Split('\n'))
        {
            if(skip_header)
            {
                skip_header = false;
                continue;
            }
            var tokens = line.Trim().Split(",");
            if(tokens.Length!=3)
                continue;
            int MovieID = int.Parse(tokens[0]);
            string MovieName = tokens[1];
            string[] GenresSplit = tokens[2].Split("|");
            List<Genre> movieGenres = new List<Genre>();
            foreach(string genre in GenresSplit)
            {
                Genre? g = genres.Find(g => g.Name == genre);
                if (g == null)
                {
                    g = new Genre();
                    g.Name = genre;
                    g.GenreID = genres.Count() + 1;

                    genres.Add(g);
                }
                movieGenres.Add(g);
            }

            if (movies.Find(e => e.MovieID == MovieID) == null)
            {
                Movie m = new Movie();
                m.MovieID = MovieID;
                m.Title = MovieName;
                m.Genres = movieGenres;

                movies.Add(m);
            }
        }

        foreach (Genre genre in genres)
        {
            dbContext.Genres.Add(genre);
        }
        dbContext.SaveChanges();

        foreach (Movie movie in movies)
        {
            dbContext.Movies.Add(movie);
        }
        dbContext.SaveChanges();

        return"OK";
    }

    [HttpPost("UploadRatingCsv")]
    public string UploadRatingCsv(IFormFile inputFile)
    {
        var strm = inputFile.OpenReadStream();
        byte[] buffer = new byte[inputFile.Length];
        strm.Read(buffer, 0, (int)inputFile.Length);
        string fileContent = System.Text.Encoding.Default.GetString(buffer);
        strm.Close();

        MoviesContext dbContext = new MoviesContext();

        bool skip_header = true;
        List<User> users = new List<User>();
        List<Rating> ratings = new List<Rating>();
        List<Movie> movies = dbContext.Movies.AsEnumerable().ToList();
        foreach(string line in fileContent.Split('\n'))
        {
            if(skip_header)
            {
                skip_header = false;
                continue;
            }
            var tokens = line.Trim().Split(",");
            if(tokens.Length!=4)
                continue;
            int UserID = int.Parse(tokens[0]);
            int MovieID = int.Parse(tokens[1]);
            int Rating =  (int)(float.Parse(tokens[2]) * 2.0f);

            User? user = users.Find(u => u.UserID == UserID);
            if (user == null)
            {
                user = new User();
                user.UserID = UserID;
                users.Add(user);
            }

            Movie? movie = movies.Find(m => m.MovieID == MovieID);

            Rating r = new Rating();
            r.RatingID = ratings.Count() + 1;
            r.RatingValue = Rating;
            r.RatingUser = user;
            r.RatedMovie = movie;

            ratings.Add(r);
        }

        foreach (User user in users)
        {
            dbContext.Users.Add(user);
        }
        dbContext.SaveChanges();

        foreach (Rating rating in ratings)
        {
            dbContext.Ratings.Add(rating);
        }
        dbContext.SaveChanges();

        return"OK";
    }

    [HttpGet("GetAllGenres")]
    public IEnumerable<Genre> GetAllGenres()
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Genres.AsEnumerable();
    }

    [HttpGet("GetMoviesByName/{search_phrase}")]
    public IEnumerable<Movie> GetMoviesByName(string search_phrase)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies.Where(e => e.Title.Contains(search_phrase));
    }

    [HttpPost("GetMoviesByGenre")]
    public IEnumerable<Movie> GetMoviesByGenre(string search_phrase)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies.Where(m=>m.Genres.Any(p=>p.Name.Contains(search_phrase)));
    }

    [HttpGet("GetGenresByMovie/{movieID}")]
    public IEnumerable<Genre> GetGenresByMovie(int movieID)
    {
        MoviesContext dbContext = new MoviesContext();
        IEnumerable<Genre> genres = dbContext.Movies.Where(m=>m.MovieID==movieID).SelectMany(m=>m.Genres);
        return genres;
    }

    [HttpGet("GetGenresVectorByMovie/{movieID}")]
    public int[] GetGenresVectorByMovie(int movieID)
    {
        MoviesContext dbContext = new MoviesContext();
        IEnumerable<Genre> movieGenres = GetGenresByMovie(movieID);
        int[] vec = new int[dbContext.Genres.Max(g => g.GenreID)];
        foreach (Genre genre in movieGenres)
        {
            vec[genre.GenreID-1] = 1;
        }

        return vec;
    }

    [HttpGet("GetCosineSimilarity/{movieID1}/{movieID2}")]
    public double GetCosineSimilarity(int movieID1, int movieID2)
    {
        int[] vec1 = GetGenresVectorByMovie(movieID1);
        int[] vec2 = GetGenresVectorByMovie(movieID2);

        return cosineSimilarity(vec1, vec2);
    }

    private double cosineSimilarity(int[] vec1, int[] vec2)
    {
        int[] bothVec = vec1.Zip(vec2, (a, b) => a * b).ToArray();
        double vec1Length = 0.0;
        double vec2Length = 0.0;
        for (int i = 0; i < vec1.Length; i++) {
            if (vec1[i] == 0 && vec2[i] == 0)
                continue;
            vec1Length += vec1[i] * vec1[i];
            vec2Length += vec2[i] * vec2[i];
        }
        vec1Length = Math.Sqrt(vec1Length);
        vec2Length = Math.Sqrt(vec2Length);

        double cosineSimilarity = bothVec.Sum() / (vec1Length * vec2Length);
        return cosineSimilarity;
    }

    [HttpGet("GetMoviesWithSameGenre/{movieID}")]
    public IEnumerable<Movie> GetMoviesWithSameGenre(int movieID)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies
            .Where(m => m.MovieID == movieID)
            .SelectMany(m => m.Genres)
            .SelectMany(g => g.Movies)
            .Where(m => m.MovieID != movieID)
            .Distinct();
    }

    [HttpGet("GetSimilarWithThreshold/{threshold}/{movieID}")]
    public IEnumerable<Movie> GetSimilarWithThreshold(double threshold, int movieID){
        MoviesContext dbContext = new MoviesContext();
        var moviesGenres = dbContext.Movies.Select(m=>new {m.MovieID, m.Genres});
        int[] movieVec = GetGenresVectorByMovie(movieID);
        int len = dbContext.Genres.Count();
        List<int> recommendIds = new List<int>();
        foreach (var movieGenre in moviesGenres) {
            int[] movieGenreVec = new int[len];
            foreach (Genre genre in movieGenre.Genres) {
                movieGenreVec[genre.GenreID-1] = 1;
            }
            double similarity = cosineSimilarity(movieVec, movieGenreVec);
            if(similarity > threshold) {
                recommendIds.Add(movieGenre.MovieID);
            }
        }
        return dbContext.Movies.Where(m=>recommendIds.Contains(m.MovieID));
    }

    // method returns a list of movies rated by a user with a given id
    [HttpGet("GetMoviesRatedByUser/{userID}")]
    public IEnumerable<Movie?> GetMoviesRatedByUser(int userID) {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Ratings
            .Where(r => r.RatingUser == null ? false : r.RatingUser.UserID == userID)
            .Where(r => r.RatedMovie != null)
            .Select(r => r.RatedMovie);
    }

    // method  returns a list of movies rated by a user with a given id, sorted by the rating
    [HttpGet("GetMoviesRatedByUserSorted/{userID}")]
    public IEnumerable<Movie?> GetMoviesRatedByUserSorted(int userID) {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Ratings
            .Where(r => r.RatingUser == null ? false : r.RatingUser.UserID == userID)
            .Where(r => r.RatedMovie != null)
            .OrderByDescending(r => r.RatingValue)
            .Select(r => r.RatedMovie);
    }

    [HttpGet("GetSimilarMoviesByHighestRated/{userID}/{threshold}")]
    public IEnumerable<Movie> GetSimilarMoviesByHighestRated(int userID, double threshold)
    {
        MoviesContext dbContext = new MoviesContext();
        Movie? userHighestRatedMovie = GetMoviesRatedByUserSorted(userID).First();
        if (userHighestRatedMovie != null)
            return GetSimilarWithThreshold(threshold, userHighestRatedMovie.MovieID);
        else
            return new List<Movie>();
    }

    [HttpGet("GetRecommendations/{userID}/{threshold}/{count}")]
    public IEnumerable<Movie> GetRecommendations(int userID, double threshold, int count)
    {
        return GetSimilarMoviesByHighestRated(userID, threshold).Take(count);
    }

    [HttpGet("GetRatingsVectorByUser/{userID}")]
    public int[] GetRatingsVectorByUser(int userID)
    {
        MoviesContext dbContext = new MoviesContext();
        var ratings = dbContext.Ratings
            .Where(r => r.RatingUser == null ? false : r.RatingUser.UserID == userID)
            .Where(r => r.RatedMovie != null)
            .Select(r => Tuple.Create(r.RatingValue, r.RatedMovie.MovieID))
            .ToList();

        int[] vec = new int[dbContext.Movies.Max(m => m.MovieID)];
        foreach (var rating in ratings)
        {
            vec[rating.Item2-1] = rating.Item1;
        }

        return vec;
    }

    public class SimilarUser
    {
        public User user {get; set;}
        public double similarity {get; set;}
    }
    
    [HttpGet("GetSimilarUsers/{userID}/{count}")]
    public IEnumerable<User> GetSimilarUsers(int userID, int count)
    {
        int[] ratingsVec = GetRatingsVectorByUser(userID);

        MoviesContext dbContext = new MoviesContext();
        var UsersRatings = dbContext.Ratings
            .Where(r => r.RatingUser != null && r.RatedMovie != null)
            .Select(r => new {r.RatingUser, r.RatingValue, r.RatedMovie!.MovieID});
        
        int usersMaxIdx = dbContext.Users.Max(u => u.UserID);
        int moviesMaxIdx = dbContext.Movies.Max(m => m.MovieID);

        int[,] userRatings = new int[usersMaxIdx, moviesMaxIdx];
        User[] usersByID = new User[usersMaxIdx];

        foreach (var item in UsersRatings)
        {
            userRatings[item.RatingUser.UserID-1, item.MovieID-1] = item.RatingValue;
            usersByID[item.RatingUser.UserID-1] = item.RatingUser;
        }

        List<SimilarUser> similarUsers = new List<SimilarUser>();
        for (int i = 0; i < userRatings.GetLength(0); ++i)
        {
            int[] ratings = new int[userRatings.GetLength(1)];
            for (int j = 0; j < userRatings.GetLength(1); j++)
            {
                ratings[j] = userRatings[i, j];
            }
            
            SimilarUser similarUser = new SimilarUser();
            similarUser.user = usersByID[i];
            similarUser.similarity = cosineSimilarity(ratingsVec, ratings);

            similarUsers.Add(similarUser);
        }
        var similarUsersOrdered = similarUsers.OrderByDescending(u => u.similarity).ToList();

        List<User> users = new List<User>();
        for (int i = 0; i < similarUsersOrdered.Count() && users.Count() < count; ++i)
        {
            if (similarUsersOrdered[i].user.UserID != userID)
                users.Add(similarUsersOrdered[i].user);
        }
        return users;
    }

    [HttpGet("GetRecomendationsBySimilarUsers/{userID}/{numOfUsers}/{numOfMoviesPerUser}")]
    public IEnumerable<Movie> GetRecomendationsBySimilarUsers(int userID, int numOfUsers, int numOfMoviesPerUser) {
        IEnumerable<User> similarUsers = GetSimilarUsers(userID, numOfUsers);
        int[] userRatings = GetRatingsVectorByUser(userID);
        List<Movie> recommendations = new List<Movie>();

        foreach (User user in similarUsers)
        {
            IEnumerable<Movie?> userMovies = GetMoviesRatedByUserSorted(user.UserID).Take(numOfMoviesPerUser);
            foreach (Movie? movie in userMovies)
            {
                if (movie != null)
                {
                    if (userRatings[movie.MovieID-1] == 0)
                        recommendations.Add(movie);
                }
            }
        }

        return recommendations;
    }

    // T3
    [HttpGet("GetT3RecommendationsForUser/{userID}")]
    public IEnumerable<Movie> GetT3RecommendationsForUser(int userID)
    {
        MoviesContext dbContext = new MoviesContext();
        var treshold = 0.95;
        int[] topMovieIdsOfSimilarUsers = GetRecomendationsBySimilarUsers(1, 3, 1).Select(m=>m.MovieID).ToArray();
        //return dbContext.Movies.Where(m=>topMovieIdsOfSimilarUsers.Contains(m.MovieID));
        var moviesGenres = dbContext.Movies
            .Where(m=>topMovieIdsOfSimilarUsers.Contains(m.MovieID))
            .Select(m=>new {m.MovieID, m.Genres});
        int len = dbContext.Genres.Count();
        List<int> recommendIds = new List<int>();
        foreach (var MovieID in topMovieIdsOfSimilarUsers) {
            int[] movieVec = GetGenresVectorByMovie(MovieID);
            foreach (var movieGenre in moviesGenres) {
                int[] movieGenreVec = new int[len];
                foreach (Genre genre in movieGenre.Genres) {
                    movieGenreVec[genre.GenreID-1] = 1;
                }
                double similarity = cosineSimilarity(movieVec, movieGenreVec);
                if(similarity > treshold) {
                    recommendIds.Add(movieGenre.MovieID);
                }
            }
        }
        
        var recommendedMovies = dbContext.Movies.Where(m=>recommendIds.Contains(m.MovieID));

        var userMovies = GetMoviesRatedByUser(userID);
        return recommendedMovies.Except(userMovies).Distinct();
    }
}
