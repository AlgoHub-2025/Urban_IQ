# Model Artifact Inventory

### population_density_model.joblib
- **Path:** e:/Lahore HackaThone/models\population\population_density_model.joblib
- **Type:** RandomForestRegressor
- **Info:** Features expected: ['longitude', 'latitude', 'dist_to_center_km', 'north_of_center', 'east_of_center', 'lat_x_lon']

### road_type_model.joblib
- **Path:** e:/Lahore HackaThone/models\roads\road_type_model.joblib
- **Type:** Pipeline
- **Info:** Classes: ['primary', 'secondary', 'tertiary']

### label_encoder.joblib
- **Path:** e:/Lahore HackaThone/models\schools\label_encoder.joblib
- **Type:** LabelEncoder
- **Info:** Classes: ['college', 'school', 'university']

### scaler.joblib
- **Path:** e:/Lahore HackaThone/models\schools\scaler.joblib
- **Type:** StandardScaler
- **Info:** Features expected: ['lat', 'lon', 'dist_to_center_km', 'north_of_center', 'east_of_center', 'neighbors_within_1_5km']

### school_type_model.joblib
- **Path:** e:/Lahore HackaThone/models\schools\school_type_model.joblib
- **Type:** RandomForestClassifier
- **Info:** Features expected: ['lat', 'lon', 'dist_to_center_km', 'north_of_center', 'east_of_center', 'neighbors_within_1_5km'], Classes: [0, 1, 2]

### avg_humidity_percent_model.joblib
- **Path:** e:/Lahore HackaThone/models\weather\avg_humidity_percent_model.joblib
- **Type:** RandomForestRegressor
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### avg_humidity_percent_model_testfit.joblib
- **Path:** e:/Lahore HackaThone/models\weather\avg_humidity_percent_model_testfit.joblib
- **Type:** RandomForestRegressor
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### avg_temp_c_model.joblib
- **Path:** e:/Lahore HackaThone/models\weather\avg_temp_c_model.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### avg_temp_c_model_testfit.joblib
- **Path:** e:/Lahore HackaThone/models\weather\avg_temp_c_model_testfit.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### max_wind_kmh_model.joblib
- **Path:** e:/Lahore HackaThone/models\weather\max_wind_kmh_model.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### max_wind_kmh_model_testfit.joblib
- **Path:** e:/Lahore HackaThone/models\weather\max_wind_kmh_model_testfit.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### total_rain_mm_model.joblib
- **Path:** e:/Lahore HackaThone/models\weather\total_rain_mm_model.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']

### total_rain_mm_model_testfit.joblib
- **Path:** e:/Lahore HackaThone/models\weather\total_rain_mm_model_testfit.joblib
- **Type:** LinearRegression
- **Info:** Features expected: ['avg_temp_c_lag1', 'avg_temp_c_lag2', 'avg_temp_c_lag3', 'avg_temp_c_lag7', 'avg_temp_c_roll_mean7', 'avg_temp_c_roll_std7', 'avg_humidity_percent_lag1', 'avg_humidity_percent_lag2', 'avg_humidity_percent_lag3', 'avg_humidity_percent_lag7', 'avg_humidity_percent_roll_mean7', 'avg_humidity_percent_roll_std7', 'total_rain_mm_lag1', 'total_rain_mm_lag2', 'total_rain_mm_lag3', 'total_rain_mm_lag7', 'total_rain_mm_roll_mean7', 'total_rain_mm_roll_std7', 'max_wind_kmh_lag1', 'max_wind_kmh_lag2', 'max_wind_kmh_lag3', 'max_wind_kmh_lag7', 'max_wind_kmh_roll_mean7', 'max_wind_kmh_roll_std7', 'doy_sin', 'doy_cos', 'month', 'is_monsoon']