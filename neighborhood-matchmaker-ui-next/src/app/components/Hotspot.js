import styles from '../styles/Hotspot.module.css';

const HotSpot = ({ hotspot }) => {
  const getImagePosition = (position) => {
    const positions = {
      'top-left': { top: '5%', left: '5%' },
      'top-right': { top: '5%', right: '5%' },
      'bottom-left': { bottom: '5%', left: '5%' },
      'bottom-right': { bottom: '5%', right: '5%' }
    };
    return positions[position];
  };

  const getImageClasses = (position) => {
    const classMap = {
      'top-left': styles.topLeft,
      'top-right': styles.topRight,
      'bottom-left': styles.bottomLeft,
      'bottom-right': styles.bottomRight
    };
    
    return `${styles.cornerImage} ${classMap[position]}`;
  };

  return (
    <div
      className={getImageClasses(hotspot.position)}
      style={getImagePosition(hotspot.position)}
    >
      <img 
        src={hotspot.image} 
        alt="" 
        className={styles.imageElement}
      />
    </div>
  );
};

export default HotSpot;