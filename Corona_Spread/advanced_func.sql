DELIMITER $$

CREATE PROCEDURE advanced_func()
BEGIN

   Declare done int default 0;
   Declare state_ VARCHAR(100);
   Declare date_ VARCHAR(100);
   Declare case_ real;
   Declare hospital_ real;
   Declare temperature real;
   Declare temp VARCHAR(100) default 'a';
   Declare increase_ real;
   Declare count_num real;
    
   Declare cur CURSOR for select us.state,us.date,us.cases,h.hosp_num,t.avg_temp
                        from (select u.state,u.cases,u.deaths,u.date 
									from US_Cases_Day u 
                                    where u.date in ('4/19/20','4/14/20') 
                                    order by state) us,
                              hospital_data h,temperature_data t 
                        where us.state=h.state and us.state=t.state 
                        order by us.state,us.date;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

Drop table if exists predict_death;

create table predict_death(
_state VARCHAR(100),
death_num real
);

open cur;

myloop:  LOOP

   fetch next from cur into state_,date_,case_,hospital_,temperature;
   
   IF done=1 THEN
      LEAVE myloop;
      END IF;
    
   IF temp!=state_ then
      set temp=state_;
      set increase_=case_;
   ELSE 
      set increase_=case_-increase_;
      set increase_=increase_/5;
      set count_num=increase_+case_;
      
      
		if(temperature<=42) then
		if(case_*0.061 <= hospital_*8.95) then
		insert into predict_death
		values(state_,count_num*4*0.021);
       
		else insert into pre_death
		values(state_,count_num*4*0.049);
		end if;
        
        elseif(temperature>42 and temperature<=45) then
		if(case_*0.061 <= hospital_*8.95) then
		insert into predict_death
		values(state_,count_num*3*0.021);
       
		else insert into predict_death
		values(state_,count_num*3*0.049);
		end if;
        
		elseif(temperature>45 and temperature<=51) then
		if(case_*0.061 <= hospital_*8.95) then
		insert into predict_death
		values(state_,count_num*2.5*0.021);
       
		else insert into predict_death
		values(state_,count_num*2.5*0.049);
		end if;
        
        
        elseif(temperature>51 and temperature<59) then
		if(case_*0.061 <= hospital_*8.95) then
		insert into predict_death
		values(state_,count_num*2.2*0.021);
       
		else insert into predict_death
		values(state_,count_num*2.2*0.049);
		end if;


		elseif(temperature>=59) then
		if(case_*0.061 <= hospital_*8.95) then
		insert into predict_death
		values(state_,count_num*2*0.021);
       
		else insert into predict_death
		values(state_,count_num*2*0.049);
		end if;
		
        end if;
      
   END IF;
    
	END LOOP;
    
    select * from predict_death;

END$$

DELIMITER ;