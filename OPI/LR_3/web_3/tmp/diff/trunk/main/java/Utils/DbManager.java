    package Utils;

    import java.io.IOException;
    import java.io.InputStream;
    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.SQLException;
    import java.sql.Statement;
    import java.util.Properties;
    import java.util.logging.Level;
    import java.util.logging.Logger;
    import java.util.ResourceBundle;

    public class DbManager {
        private static final ResourceBundle messages =
                ResourceBundle.getBundle("locales");

        private static final Logger logger = Logger.getLogger(DbManager.class.getName());
        private static String DB_URL = "jdbc:hsqldb:hsql://localhost:14100/web_lab3_db";
        private static String DB_USER = "SA";
        private static String DB_PASSWORD = "";

        static {
            loadProperties("database.properties");
            try {
                initializeDatabase();
            } catch (SQLException e) {
                logger.log(Level.SEVERE, messages.getString("db.init.failed"), e);
            }
        }
        static void loadProperties(String fileName) {
            try (InputStream is = DbManager.class.getClassLoader()
                    .getResourceAsStream(fileName)) {
                Properties props = new Properties();
                props.load(is);

                DB_URL = props.getProperty("db.url");
                DB_USER = props.getProperty("db.user");
                DB_PASSWORD = props.getProperty("db.password");

                logger.info("Loaded config: " + fileName);
            } catch (IOException e) {
                logger.log(Level.SEVERE, "Cannot load " + fileName, e);
            }
        }
        public static Connection getConnection() throws SQLException {
            return DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
        }

        private static void initializeDatabase() throws SQLException {
            try (Connection conn = getConnection()) {
                String createTableSQL =
                    "CREATE TABLE IF NOT EXISTS points (" +
                    "id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, " +
                    "x INTEGER NOT NULL, " +
                    "y DOUBLE NOT NULL, " +
                    "r DOUBLE NOT NULL, " +
                    "result VARCHAR(50) NOT NULL, " +
                    "stime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " +
                    "rtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                    ")";

                try (Statement stmt = conn.createStatement()) {
                    stmt.execute(createTableSQL);
                    logger.info(messages.getString("db.init.success"));
                }
            }
        }

        public static void closeConnection(Connection conn) {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    logger.log(Level.WARNING, messages.getString("db.close.error"), e);
                }
            }
        }
    }

