def opponent(cp, previous_cp, best_cp):
    diff1 = cp - previous_cp
    diff2 = best_cp-cp
 
    
    value = ''  # Default value
    if diff2==0:
        value="best move"
    elif diff1>0:

    # Condition checks
        
        if (abs(diff2)<4 or -diff2>0):
            value = 'best move'
        elif abs(diff2)<10 and diff1 > 300:
            value = 'brilliant'
        elif diff1 > 150 and abs(diff2)<10:
            value = 'great move'
        elif diff1 > 50 and abs(diff2)<10:
            value = 'nice move'
   
        elif diff1 >= 0:
            value = 'good'
    else:
        if diff2<0:
            if (abs(diff2)<4 or -diff2>0):
                value = 'best move'
            
           
    
            elif abs(diff2)<15:
                value = 'good'
            if diff2 > 500:
                value = 'You Missed'
            elif diff2 > 300:
                value = 'blunder'
            elif diff2 >100 and diff1 < -100:
                value = 'worst move'
            elif diff2 >15:
                value = 'inaccuracy'
            elif diff2 > 8:
                value = 'not Good'
        else:
            if diff2 > 500:
                value = 'You Missed'
            elif diff2 > 300:
                value = 'blunder'
            elif diff2 >100 and diff1 < -100:
                value = 'worst move'
            elif diff2 > 50:
                value = 'mistake'
            elif diff2 >10 and diff1<-10:
                value = 'inaccuracy'
            elif diff1 < 0:
                value = 'not Good'
    
    # If no condition is met, assign a default value
    if value == '':
        value = 'neutral'  # Or any default value you prefer
    
    return value
