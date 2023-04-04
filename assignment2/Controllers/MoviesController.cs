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
    public short[] GetGenresVectorByMovie(int movieID)
    {
        IEnumerable<Genre> movieGenres = GetGenresByMovie(movieID);
        IEnumerable<Genre> allGenres = GetAllGenres();
        short[] vec = new short[allGenres.Count()];
        foreach (Genre genre in movieGenres)
        {
            vec[genre.GenreID-1] = 1;
        }

        return vec;
    }
}