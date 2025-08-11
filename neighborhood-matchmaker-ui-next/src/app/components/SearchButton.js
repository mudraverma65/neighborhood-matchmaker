import styles from '../styles/HomePage.module.css';

export default function SearchButton(){
    // const [searchButtonClicked, handleSearch] = useState(null);
    
    const handleSearch = () => {
        // searchButtonClicked = true;
        console.log('Opening search form...');
    };
    return (
        <div style={styles.centerContainer}>
          <div style={styles.titleSection}>
            <h1 style={styles.mainTitle}>Find Your</h1>
            <h1 style={styles.accentTitle}>Montreal Vibe</h1>
          </div>
          
          <button
            onClick={handleSearch}
            style={styles.searchButton}
            onMouseEnter={(e) => {
              e.target.style.transform = 'scale(1.05) rotate(2deg)';
              e.target.style.boxShadow = '0 20px 40px rgba(0,0,0,0.3)';
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'scale(1) rotate(0deg)';
              e.target.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
            }}
          >
            <div style={styles.buttonShine}></div>
            <span style={styles.buttonContent}>
              <span style={styles.searchEmoji}>🔍</span>
              START EXPLORING
              <span style={styles.sparkleEmoji}>✨</span>
            </span>
          </button>

          <p style={styles.subtitle}>
            Discover neighborhoods that match your lifestyle
          </p>
        </div>
    )
}