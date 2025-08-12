'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { fetchNeighborhoods, searchNeighborhoods } from '../api/apis';
import styles from '../styles/SearchForm.module.css';

const SearchForm = ({ isOpen, onClose }) => {
  const router = useRouter();

  const [errors, setErrors] = useState({});

  const [formData, setFormData] = useState({
    budget: '',
    city: 'Montreal',
    max_commute_time: '',
    destination_neighborhood: '',
    amenities: [],
    rent_types: [],
    preferred_neighborhoods:[]
  });

  const [neighborhoods, setNeighborhoods] = useState([]);

  useEffect(() => {
    fetchNeighborhoods()
      .then(setNeighborhoods)
      .catch(console.error);
  }, []);

  const amenityOptions = [
    { type: 'park', name: 'Parks', icon: '🌳', color: '#4A7C59' },
    { type: 'school', name: 'Schools', icon: '🎓', color: '#B8D4E3' },
    { type: 'restaurant', name: 'Restaurants', icon: '🍽️', color: '#FF6B6B' },
    { type: 'transit', name: 'Transit', icon: '🚇', color: '#4ECDC4' },
    { type: 'grocery', name: 'Grocery', icon: '🛒', color: '#C4D63A' },
    { type: 'hospital', name: 'Hospital', icon: '🏥', color: '#F4A6CD' },
    { type: 'cafe', name: 'Cafes', icon: '☕', color: '#FF6B6B' },
    { type: 'library', name: 'Libraries', icon: '📚', color: '#B8D4E3' },
    { type: 'gym', name: 'Gyms', icon: '💪', color: '#4ECDC4' }
  ];

  const rentTypeOptions = [
    { type: 'studio', name: 'Studio', icon: '🏠', color: '#C4D63A' },
    { type: 'One Bed', name: '1 Bedroom', icon: '🛏️', color: '#B8D4E3' },
    { type: 'Two Bed', name: '2 Bedrooms', icon: '🏡', color: '#F4A6CD' },
    { type: 'Three Bed', name: '3+ Bedrooms', icon: '🏘️', color: '#4ECDC4' }
  ];

  const handleAmenityToggle = (amenityType) => {
    setFormData(prev => ({
      ...prev,
      amenities: prev.amenities.includes(amenityType)
        ? prev.amenities.filter(a => a !== amenityType)
        : [...prev.amenities, amenityType]
    }));
  };

  const handleRentTypeToggle = (rentType) => {
    setFormData(prev => ({
      ...prev,
      rent_types: prev.rent_types.includes(rentType)
        ? prev.rent_types.filter(r => r !== rentType)
        : [...prev.rent_types, rentType]
    }));
  };

  const handleNeighborhoodToggle = (neighborhood) => {
    setFormData(prev => ({
      ...prev,
      preferred_neighborhoods: prev.preferred_neighborhoods.includes(neighborhood)
        ? prev.preferred_neighborhoods.filter(n => n !== neighborhood)
        : [...prev.preferred_neighborhoods, neighborhood]
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.budget || Number(formData.budget) <= 0) {
      newErrors.budget = true;
    }

    const hasDestination = formData.destination_neighborhood.trim() !== '';
    const hasCommute = formData.max_commute_time !== '' && Number(formData.max_commute_time) > 0;

    if (hasDestination && !hasCommute) {
      newErrors.max_commute_time = true;
    }

    if (hasCommute && !hasDestination) {
      newErrors.destination_neighborhood = true;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    try {
      const results = await searchNeighborhoods(formData);

      localStorage.setItem('searchResults', JSON.stringify(results));
      localStorage.setItem('searchCriteria', JSON.stringify(formData));
      
      router.push("/results");
    } catch (err) {
      console.error("Error searching neighborhoods:", err);
    }
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContainer}>
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitle}>Find Your Perfect Montreal Neighborhood</h2>
          <button className={styles.closeButton} onClick={onClose}>×</button>
        </div>
        
        <div className={styles.searchForm}>
          {/* Basic Info Section */}
          <div className={styles.formSection}>
            <h3 className={styles.sectionTitle}>📍 Basic Details</h3>
            <div className={styles.formGrid}>
              <div className={styles.formGroup}>
                <label className={styles.formLabel}>Budget (Monthly) <span className={styles.required}>*</span> </label>
                <div className={styles.inputWrapper}>
                  <span className={styles.inputPrefix}>$</span>
                  <input
                    type="number"
                    className={`${styles.formInput} ${errors.budget ? styles.errorInput : ''}`}
                    value={formData.budget}
                    onChange={(e) => setFormData(prev => ({...prev, budget: e.target.value}))}
                  />
                </div>
              </div>
              
              <div className={styles.formGroup}>
                <label className={styles.formLabel}>
                  Max Commute Time {errors.max_commute_time && <span className={styles.required}>*</span>}
                </label>
                <div className={styles.inputWrapper}>
                  <input
                    type="number"
                    className={`${styles.formInput} ${errors.max_commute_time ? styles.errorInput : ''}`}
                    value={formData.max_commute_time}
                    onChange={(e) => setFormData(prev => ({ ...prev, max_commute_time: e.target.value }))}
                  />
                  <span className={styles.inputSuffix}>min</span>
                </div>
              </div>

            </div>

            <select
              className={`${styles.formInput} ${styles.fullWidth} ${errors.destination_neighborhood ? styles.errorInput : ''}`}
              value={formData.destination_neighborhood}
              onChange={(e) => setFormData(prev => ({ ...prev, destination_neighborhood: e.target.value }))}
            >
              <option value="">Select destination</option>
              {neighborhoods.map((n) => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>


          </div>

          {/* Preferred Neighborhoods Section */}
          <div className={styles.formSection}>
            <h3 className={styles.sectionTitle}>🏘️ Preferred Neighborhoods</h3>
            <p className={styles.sectionDescription}>
              Select neighborhoods youd like to prioritize (optional)
            </p>
            <div className={styles.neighborhoodGrid}>
              {neighborhoods.map((neighborhood) => (
                <div
                  key={neighborhood}
                  className={`${styles.neighborhoodCard} ${formData.preferred_neighborhoods.includes(neighborhood) ? styles.selected : ''}`}
                  onClick={() => handleNeighborhoodToggle(neighborhood)}
                >
                  <div className={styles.neighborhoodName}>{neighborhood}</div>
                  <div className={styles.neighborhoodCheck}>✓</div>
                </div>
              ))}
            </div>
          </div>

          {/* Amenities Section */}
          <div className={styles.formSection}>
            <h3 className={styles.sectionTitle}>🎯 What Important to You?</h3>
            <div className={styles.cardGrid}>
              {amenityOptions.map((amenity) => (
                <div
                  key={amenity.type}
                  className={`${styles.optionCard} ${formData.amenities.includes(amenity.type) ? styles.selected : ''}`}
                  style={{'--card-color': amenity.color}}
                  onClick={() => handleAmenityToggle(amenity.type)}
                >
                  <div className={styles.cardIcon}>{amenity.icon}</div>
                  <div className={styles.cardName}>{amenity.name}</div>
                  <div className={styles.cardCheck}>✓</div>
                </div>
              ))}
            </div>
          </div>

          {/* Rent Type Section */}
          <div className={styles.formSection}>
            <h3 className={styles.sectionTitle}>🏠 What Size Place?</h3>
            <div className={styles.cardGrid}>
              {rentTypeOptions.map((rentType) => (
                <div
                  key={rentType.type}
                  className={`${styles.optionCard} ${formData.rent_types.includes(rentType.type) ? styles.selected : ''}`}
                  style={{'--card-color': rentType.color}}
                  onClick={() => handleRentTypeToggle(rentType.type)}
                >
                  <div className={styles.cardIcon}>{rentType.icon}</div>
                  <div className={styles.cardName}>{rentType.name}</div>
                  <div className={styles.cardCheck}>✓</div>
                </div>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className={styles.formActions}>
            <button type="button" className={styles.cancelButton} onClick={onClose}>
              Cancel
            </button>
            <button type="button" className={styles.submitButton} onClick={handleSubmit}>
              <span className={styles.buttonIcon}>🔍</span>
              Find My Neighborhood
              <span className={styles.buttonSparkle}>✨</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchForm;