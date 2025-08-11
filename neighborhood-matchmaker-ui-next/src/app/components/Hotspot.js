import styles from '../styles/Hotspot.module.css';

const HotSpot = ({ hotspot, isHovered, onHover, onLeave }) => {
  const getStickerPosition = (position) => {
    const positions = {
      'top-left': { top: '15%', left: '10%' },
      'top-right': { top: '12%', right: '8%' },
      'bottom-left': { bottom: '18%', left: '12%' },
      'bottom-right': { bottom: '15%', right: '10%' }
    };
    return positions[position];
  };

  const getStickerSize = (size) => {
    const sizes = {
      small: { width: '140px', height: '120px' },
      medium: { width: '180px', height: '160px' },
      large: { width: '220px', height: '190px' }
    };
    return sizes[size];
  };

  const getStickerClasses = () => {
    let classes = [styles.sticker];
    
    if (hotspot.shape) {
      classes.push(styles[`shape${hotspot.shape.charAt(0).toUpperCase() + hotspot.shape.slice(1)}`]);
    }
    
    if (hotspot.size) {
      classes.push(styles[`size${hotspot.size.charAt(0).toUpperCase() + hotspot.size.slice(1)}`]);
    }
    
    if (isHovered) {
      classes.push(styles.hovered);
    }
    
    return classes.join(' ');
  };

  const getImageClasses = () => {
    let classes = [styles.stickerImage];
    
    if (hotspot.shape === 'star') {
      classes.push(styles.starImage);
    }
    
    return classes.join(' ');
  };

  return (
    <div
      className={getStickerClasses()}
      style={{
        ...getStickerPosition(hotspot.position),
        ...getStickerSize(hotspot.size),
        backgroundColor: hotspot.color,
      }}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
    >
      <div className={styles.stickerContent}>
        <div 
          className={getImageClasses()}
          style={{
            backgroundImage: `url(${hotspot.image})`,
          }}
        ></div>
        <div className={styles.stickerText}>{hotspot.name}</div>
      </div>
      <div className={styles.stickerShadow}></div>
    </div>
  );
};

export default HotSpot;