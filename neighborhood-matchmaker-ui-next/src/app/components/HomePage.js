'use client';

import { useState } from 'react';
import styles from '../styles/HomePage.module.css';
import HotSpot from './Hotspot';
import SearchForm from './SearchForm';

const HomePage = () => {
  const [hoveredSticker, setHoveredSticker] = useState(null);
  const [isSearchOpen, setIsSearchOpen] = useState(false); // <-- new state

  const handleSearchClick = () => {
    setIsSearchOpen(true);
  };

  const handleCloseSearch = () => {
    setIsSearchOpen(false);
  };

  const hotspots = [
    {
      id: 1,
      name: "Old Montreal",
      image: "https://images.unsplash.com/photo-1549340748-6d9ac911ad70?w=400&h=300&fit=crop&crop=center",
      color: "#B8D4E3",
      position: "top-left",
      shape: "star",
      size: "large"
    },
    {
      id: 2,
      name: "Plateau",
      image: "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?w=400&h=300&fit=crop&crop=center",
      color: "#F4A6CD",
      position: "top-right",
      shape: "cloud",
      size: "medium"
    },
    {
      id: 3,
      name: "Downtown",
      image: "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=400&h=300&fit=crop&crop=center",
      color: "#FF6B6B",
      position: "bottom-left",
      shape: "thought",
      size: "small"
    },
    {
      id: 4,
      name: "Mile End",
      image: "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400&h=300&fit=crop&crop=center",
      color: "#4ECDC4",
      position: "bottom-right",
      shape: "star",
      size: "medium"
    }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.background}>
        
        {/* Floating background shapes */}
        <div className={styles.floatingShapes}>
          <div className={`${styles.floatingShape} ${styles.shape1}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape2}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape3}`}></div>
          <div className={`${styles.floatingShape} ${styles.shape4}`}></div>
        </div>

        {/* Montreal Hotspot Stickers */}
        {hotspots.map((hotspot) => (
          <HotSpot
            key={hotspot.id}
            hotspot={hotspot}
            isHovered={hoveredSticker === hotspot.id}
            onHover={() => setHoveredSticker(hotspot.id)}
            onLeave={() => setHoveredSticker(null)}
          />
        ))}

        {/* Central Search Button */}
        <div className={styles.centerContainer}>
          <div className={styles.titleSection}>
            <h1 className={styles.mainTitle}>Find Your</h1>
            <h1 className={styles.accentTitle}>Montreal Vibe</h1>
          </div>
          
          <button
            onClick={handleSearchClick}
            className={styles.searchButton}
          >
            <div className={styles.buttonShine}></div>
            <span className={styles.buttonContent}>
              <span className={styles.searchEmoji}>🔍</span>
              START EXPLORING
              <span className={styles.sparkleEmoji}>✨</span>
            </span>
          </button>

          <p className={styles.subtitle}>
            Discover neighborhoods that match your lifestyle
          </p>
        </div>

        {/* Decorative elements */}
        <div className={styles.decorativeElements}>
          <div className={`${styles.decorElement} ${styles.decor1}`}>🍁</div>
          <div className={`${styles.decorElement} ${styles.decor2}`}>🏔️</div>
          <div className={`${styles.decorElement} ${styles.decor3}`}>❄️</div>
        </div>

        {isSearchOpen && (
          <SearchForm isOpen={true} onClose={handleCloseSearch} />
        )}
      </div>
    </div>
  );
};

export default HomePage;