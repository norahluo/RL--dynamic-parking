import numpy as np
from datetime import datetime, timedelta

EARTH_D = 7917.5 # mi
LAT_D, LON_D = 69, 54.6
MAX_E = 10
VOT = 0.1
SPEED = 30
LOSS_COST = 10
THRESH_MIN, THRESH_MAX = 0, 1
P_MIN, P_MAX = 0.5, 8

class parking_block():
    def __init__(self, params, dist):
        # params are from csv file
        # dist records the distance between each two blocks

        self.block_id = params['BLOCKFACE_ID']
        self.loc = (params['LONGITUDE'], params['LATITUDE'])
        self.capacity = params['SPACE_NUM']
        self.rate_area = params['OLD_RATE_AREA_id']
        self.occupied = 0   # the count of occupied meters
        self.dist = np.sort(dist)
        self.backup_block = np.argsort(dist)    # the priority of back-up blocks

    def is_full(self):
        return self.capacity == self.occupied

    def inc_v(self):
        self.occupied += 1

    def dec_v(self):
        self.occupied -= 1

    def reset(self):
        self.occupied = 0

    def __str__(self):
        return 'Block {id} {loc}\nOccupancy: {occ}/{cap}'.format(
                    id=self.block_id, loc=self.loc,
                    occ=self.occupied, cap=self.capacity)

class vehicle():
    def __init__(self, params):
        self.loc_arrive = params['id']
        self.price_thresh = np.random.uniform(THRESH_MIN, THRESH_MAX)
        self.ind_loc_current = 0
        self.cruising_dist = 0
        self.parked = False
        self.fee = 0
        self.remaining_time = 0

    def dec_time(self):
        self.remaining_time = max(0, self.remaining_time - 1)

    def inc_ind_loc(self):
        self.ind_loc_current += 1

    def __str__(self):
        return 'Vehicle arrived at Block {arr}\n{parked}parked{text}'.format(
                    arr=self.loc_arrive, parked='' if self.parked else 'not',
                    text=' at the {cur}-th nearest block with total cruising distance {dist}\nThe remaining parking time is {rt}.'.format(
                        cur=self.ind_loc_current, dist=self.cruising_dist, rt=self.remaining_time) if self.parked else '')

class parking_env():
    def __init__(self, df_block, df_demand):
        self.date = datetime(2019,12,1)
        self.slot = 0
        self.stage = 0
        self.df_demand = df_demand
        # mat_distance = self.great_circle_v(df_block['LONGITUDE'].values, df_block['LATITUDE'].values)
        mat_distance = self.manhattan_v(df_block['LONGITUDE'].values, df_block['LATITUDE'].values)
        self.blocks = [parking_block(record, mat_distance[i]) for i, record in enumerate(df_block.to_dict('records'))]
        self.vehicles = np.empty(0)
        self.ob_dim = 2 + len(self.blocks)
        self.ac_dim = len(df_block['OLD_RATE_AREA_id'].unique())

    def seed(self, s):
        np.random.seed(s)

    def identify_stage(self, dt):
        if dt < datetime(2020, 3, 15):
            return 0  # before
        elif (dt >= datetime(2020, 3, 15)) & (dt < datetime(2020, 5, 17)):
            return 1  # shutdown
        elif (dt >= datetime(2020, 5, 17)) & (dt < datetime(2020, 7, 17)):
            return 2  # reopen
        elif (dt >= datetime(2020, 7, 17)) & (dt < datetime(2020, 9, 30)):
            return 3  # closed_due_to_state_re
        elif (dt >= datetime(2020, 9, 30)) & (dt < datetime(2020, 10, 20)):
            return 4  # orange
        elif (dt >= datetime(2020, 10, 20)) & (dt < datetime(2020, 11, 13)):
            return 5  # yellow
        elif dt >= datetime(2020, 11, 13):
            return 6  # rollback

    def cal_linear_coef(self, area):
        if area == 2:
            return 1200.6071  # downtown
        elif area == 3:
            return 0  # near downtown
        elif area == 1:
            return -1798.1531  # Residential
        elif area in [4, 15, 13]:
            return -102.1678  # Fisherman's Wharf
        elif area in [10, 5]:
            return 1454.1244  # North Embarcadero
        elif area in [9, 7, 11, 14]:
            return 2164.0275  # downtown port
        elif area in [12, 6, 8]:
            return 2935.8303  # South Embarcadero
        else:
            return 0

    # calculate the great circle distance for all the blocks with matrix form
    def great_circle_v(self, lon, lat):
        lon, lat = np.radians(lon), np.radians(lat)
        return EARTH_D * np.arccos(np.sin(lat) * np.sin(lat).reshape(-1, 1) \
                + np.cos(lat) * np.cos(lat).reshape(-1, 1) * np.cos(lon-lon.reshape(-1, 1)))

    def manhattan_v(self, lon, lat):
        return LON_D * np.abs(lon-lon.reshape(-1, 1)) + LAT_D * np.abs(lat-lat.reshape(-1, 1))

    # generate demand for each block at time t
    def generate_demand(self):
        df = self.df_demand[(self.df_demand['slot'] == self.slot) & (self.df_demand['stage'] == self.stage)]
        d = np.random.poisson(df['mean'].values, len(df))
        return d

    def simulate_v_park(self, v, p):
        ind_cur_block = self.blocks[v.loc_arrive].backup_block[v.ind_loc_current]
        if (not self.blocks[ind_cur_block].is_full()) | (p[self.blocks[ind_cur_block].rate_area] <= v.price_thresh):
            v.parked = True
            self.blocks[ind_cur_block].inc_v()
            parking_time = np.random.normal((self.cal_linear_coef(self.blocks[ind_cur_block]) + 7820.5177
                            - 820.3637*p[self.blocks[ind_cur_block].rate_area]) / 3600, 1.28)
            v.remaining_time = max(parking_time * 2, 0)
            v.fee = v.remaining_time * p[self.blocks[ind_cur_block].rate_area]
        else:
            v.inc_ind_loc()
            new_ind_block = self.blocks[v.loc_arrive].backup_block[v.ind_loc_current]
            v.cruising_dist = self.blocks[ind_cur_block].dist[new_ind_block]

    # simulate the parking behavior with choice model
    def do_simulation(self, a):
        self.date = self.date + timedelta(minutes=30)
        self.slot = self.date.hour * 2 + (1 if int(self.date.minute) < 30 else 2) - 1
        self.stage = self.identify_stage(self.date)

        # parked vehicles
        ind_vehicles = []
        for i, v in enumerate(self.vehicles):
            v.dec_time()
            if v.remaining_time == 0:
                ind_cur_block = self.blocks[v.loc_arrive].backup_block[v.ind_loc_current]
                self.blocks[ind_cur_block].dec_v()
            else:
                ind_vehicles.append(i)
        self.vehicles = self.vehicles[ind_vehicles]

        # parking vehicles
        num_parked_vehicles = len(self.vehicles)
        d = self.generate_demand()
        for i, block in enumerate(self.blocks):
            self.vehicles = np.append(self.vehicles, [vehicle({'id': i}) for _ in range(d[i])])
        for t_e in range(MAX_E-1):
            for v in self.vehicles[num_parked_vehicles:]:
                if not v.parked:
                    self.simulate_v_park(v, P_MIN + (P_MAX-P_MIN) * a)

        reward = 0
        for v in self.vehicles[num_parked_vehicles:]:
            if v.parked:
                reward += v.fee - v.cruising_dist / SPEED * VOT
            else:
                reward -= LOSS_COST

        return reward

    # given the action, simulate the process and get the reward
    def step(self, a):
        reward = self.do_simulation(a)
        ob = self._get_obs()
        done = self.date >= datetime(2020, 11, 30)
        return ob, reward, done, None

    def _get_obs(self):
        return np.concatenate([[self.stage, self.slot], [block.occupied for block in self.blocks]])

    def reset_model(self):
        self.date = datetime(2019,12,1) + timedelta(np.random.randint(0, 366))
        self.stage = self.identify_stage(self.date)
        self.vehicles = np.empty(0)
        for b in self.blocks:
            b.reset()
        return self._get_obs()

    def reset(self):
        ob = self.reset_model()
        return ob

    def __str__(self):
        return '{t}, there are {num_b} blocks and {num_v} vehicles.'.format(
                    t=self.date, num_b=len(self.blocks), num_v=len(self.vehicles))