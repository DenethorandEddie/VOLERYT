import React from 'react';
import './TierBadge.css';

const TierBadge = ({ tier, color }) => {
  return (
    <span className={`tier-badge tier-${tier.toLowerCase().replace('+', 'plus')}`} style={{ backgroundColor: color }}>
      {tier}
    </span>
  );
};

export default TierBadge;
