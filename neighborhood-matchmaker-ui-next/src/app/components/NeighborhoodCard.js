import styles from '../styles/NeighborhoodCard.module.css';

const NeighborhoodCard = ({ neighborhood, rank }) => {
  const getTopAmenities = () => {
    return Object.entries(neighborhood.amenity_counts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 4);
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

  const getScoreColor = (score) => {
    if (score >= 80) return '#4ECDC4';
    if (score >= 60) return '#C4D63A';
    if (score >= 40) return '#FF6B6B';
    return '#F4A6CD';
  };

  return (
    <div className={styles.neighborhoodCard}>
      <div className={styles.cardHeader}>
        <div className={styles.rankBadge}>
          <span className={styles.rankText}>#{rank}</span>
        </div>
        
        <div className={styles.scoreCircle} style={{'--score-color': getScoreColor(neighborhood.score)}}>
          <span className={styles.scoreValue}>{neighborhood.score}</span>
          <span className={styles.scorePercent}>%</span>
        </div>
      </div>

      <div className={styles.cardContent}>
        <h3 className={styles.neighborhoodName}>
          {neighborhood.neighborhood_name}
        </h3>

        {neighborhood.commute_time && (
          <div className={styles.commuteInfo}>
            <span className={styles.commuteIcon}>🚇</span>
            <span className={styles.commuteText}>{neighborhood.commute_time} min commute</span>
          </div>
        )}

        <div className={styles.amenitiesGrid}>
          {getTopAmenities().map(([type, count]) => (
            <div key={type} className={styles.amenityItem}>
              <span className={styles.amenityIcon}>
                {getAmenityIcon(type)}
              </span>
              <div className={styles.amenityDetails}>
                <span className={styles.amenityCount}>{count}</span>
                <span className={styles.amenityType}>
                  {type.replace('_', ' ')}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className={styles.totalSection}>
          <div className={styles.totalAmenities}>
            <span className={styles.totalIcon}>📍</span>
            <span className={styles.totalText}>
              {neighborhood.total_amenities} total amenities
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NeighborhoodCard;