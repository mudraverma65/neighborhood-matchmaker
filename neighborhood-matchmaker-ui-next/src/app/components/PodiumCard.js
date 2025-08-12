import styles from '../styles/PodiumCard.module.css';

const PodiumCard = ({ neighborhood, position, rank }) => {
  const getMedalEmoji = (position) => {
    switch (position) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '🏆';
    }
  };

  const getPodiumHeight = (position) => {
    switch (position) {
      case 1: return 'first';
      case 2: return 'second';
      case 3: return 'third';
      default: return 'first';
    }
  };

  const getTopAmenities = () => {
    return Object.entries(neighborhood.amenity_counts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3);
  };

  const getAmenityIcon = (amenityType) => {
    const icons = {
      park: '🌳',
      school: '🎓',
      restaurant: '🍽️',
      transit: '🚇',
      grocery: '🛒',
      hospital: '🏥',
      cafe: '☕',
      library: '📚',
      gym: '💪'
    };
    return icons[amenityType] || '📍';
  };

  return (
    <div className={`${styles.podiumCard} ${styles[getPodiumHeight(position)]}`}>
      <div className={styles.medal}>
        <span className={styles.medalEmoji}>{getMedalEmoji(position)}</span>
        <span className={styles.rankNumber}>{rank}</span>
      </div>
      
      <div className={styles.cardContent}>
        <h3 className={styles.neighborhoodName}>
          {neighborhood.neighborhood_name}
        </h3>
        
        <div className={styles.score}>
          <span className={styles.scoreLabel}>Match Score</span>
          <span className={styles.scoreValue}>{neighborhood.score}%</span>
        </div>

        {neighborhood.commute_time && (
          <div className={styles.commuteTime}>
            <span className={styles.commuteIcon}>🚇</span>
            <span>{neighborhood.commute_time} min commute</span>
          </div>
        )}

        <div className={styles.amenitiesSection}>
          <h4 className={styles.amenitiesTitle}>Top Amenities</h4>
          <div className={styles.amenitiesList}>
            {getTopAmenities().map(([type, count]) => (
              <div key={type} className={styles.amenityItem}>
                <span className={styles.amenityIcon}>
                  {getAmenityIcon(type)}
                </span>
                <span className={styles.amenityText}>
                  {count} {type.replace('_', ' ')}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.totalAmenities}>
          <span className={styles.totalIcon}>📍</span>
          <span className={styles.totalText}>
            {neighborhood.total_amenities} total amenities
          </span>
        </div>
      </div>

      <div className={styles.podiumBase}>
        <span className={styles.positionLabel}>#{position}</span>
      </div>
    </div>
  );
};

export default PodiumCard;