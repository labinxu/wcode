function pow(a, b){
    return Math.pow(a,b);
}
function exp(a){
    return Math.exp(a);
}
function log(a){
    return Math.log(a);
}
function i_in_range(a, b, e){
    return (a>=b && a<=e);
}

function is_boolean(a){
    if (a == 0 || a == 1){
        return true;
    }
    return false;
}

function d_in_range(a, b, e){
    return (a>=b && a<=e);
}

function strlcat(output, msgformat, data){
    alert(msgformat);
    return msgformat+data;
}

function cvd_female_raw(age, b_AF, b_ra, b_renal, b_treatedhyp, b_type1, b_type2,
                        bmi, ethrisk, fh_cvd, rati, sbp, smoke_cat, surv, town){

    survivor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.988948762416840, 0, 0, 0, 0, 0];
    Iethrisk = [0, 0,
		            0.2671958047902151500000000,
		            0.7147534261793343500000000,
		            0.3702894474455115700000000,
		            0.2073797362620235500000000,
		            -0.1744149722741736900000000,
		            -0.3271878654368842200000000,
		            -0.2200617876129250500000000,
		            -0.2090388032466696800000000];
    Ismoke = [
		    0,
		    0.1947480856528854800000000,
		    0.6229400520450627500000000,
		    0.7405819891143352600000000,
		    0.9134392684576959600000000];
    /* Applying the fractional polynomial transforms */
	  /* (which includes scaling)                      */

	  dage = age;
	  dage=dage/10;
	  age_1 = pow(dage,.5);
	  age_2 = dage;
	  dbmi = bmi;
	  dbmi=dbmi/10;
	  bmi_1 = pow(dbmi,-2);
	  bmi_2 = pow(dbmi,-2)*log(dbmi);

    /* Centring the continuous variables */

	  age_1 = age_1 - 2.099778413772583;
	  age_2 = age_2 - 4.409069538116455;
	  bmi_1 = bmi_1 - 0.154046609997749;
	  bmi_2 = bmi_2 - 0.144072100520134;
	  rati = rati - 3.554229259490967;
	  sbp = sbp - 125.773628234863280;
	  town = town - 0.032508373260498;
    /* Start of Sum */
	  a=0;

	  /* The conditional sums */

	  a += Iethrisk[ethrisk];
	  a += Ismoke[smoke_cat];

	  /* Sum from continuous values */

	  a += age_1 * 3.8734583855051343000000000;
	  a += age_2 * 0.1346634304478384600000000;
	  a += bmi_1 * -0.1557872403333062600000000;
	  a += bmi_2 * -3.7727795566691125000000000;
	  a += rati * 0.1525695208919679600000000;
	  a += sbp * 0.0132165300119653560000000;
	  a += town * 0.0643647529864017080000000;

    /* Sum from boolean values */

	  a += b_AF * 1.4235421148946676000000000;
	  a += b_ra * 0.3021462511553648100000000;
	  a += b_renal * 0.8614743039721416400000000;
	  a += b_treatedhyp * 0.5889355458733703800000000;
	  a += b_type1 * 1.6684783657502795000000000;
	  a += b_type2 * 1.1350165062510138000000000;
	  a += fh_cvd * 0.5133972775738673300000000;

    	/* Sum from interaction terms */

	  a += age_1 * (smoke_cat==1) * 0.6891139747579299000000000;
	  a += age_1 * (smoke_cat==2) * 0.6942632802121626600000000;
	  a += age_1 * (smoke_cat==3) * -1.6952388644218186000000000;
	  a += age_1 * (smoke_cat==4) * -1.2150150940219255000000000;
	  a += age_1 * b_AF * -3.5855215448190969000000000;
	  a += age_1 * b_renal * -3.0766647922469192000000000;
	  a += age_1 * b_treatedhyp * -4.0295302811880314000000000;
	  a += age_1 * b_type1 * -0.3344110567405778600000000;
	  a += age_1 * b_type2 * -3.3144806806620530000000000;
	  a += age_1 * bmi_1 * -5.5933905797230006000000000;
	  a += age_1 * bmi_2 * 64.3635572837688980000000000;
	  a += age_1 * fh_cvd * 0.8605433761217157200000000;
	  a += age_1 * sbp * -0.0509321154551188590000000;
	  a += age_1 * town * 0.1518664540724453700000000;
	  a += age_2 * (smoke_cat==1) * -0.1765395485882681500000000;
	  a += age_2 * (smoke_cat==2) * -0.2323836483278573000000000;
	  a += age_2 * (smoke_cat==3) * 0.2734395770551826300000000;
	  a += age_2 * (smoke_cat==4) * 0.1432552287454152700000000;
	  a += age_2 * b_AF * 0.4986871390807032200000000;
	  a += age_2 * b_renal * 0.4393033615664938600000000;
	  a += age_2 * b_treatedhyp * 0.6904385790303250200000000;
	  a += age_2 * b_type1 * -0.1734316566060327700000000;
	  a += age_2 * b_type2 * 0.4864930655867949500000000;
	  a += age_2 * bmi_1 * 1.5223341309207974000000000;
	  a += age_2 * bmi_2 * -12.7413436207964070000000000;
	  a += age_2 * fh_cvd * -0.2756708481415109900000000;
	  a += age_2 * sbp * 0.0073790750039744186000000;
	  a += age_2 * town * -0.0487465462679640900000000;

    /* Calculate the score itself */
	  score = 100.0 * (1 - pow(survivor[surv], exp(a)) );
	  return score;
}
function cvd_female_validation(age, b_AF, b_ra, b_renal, b_treatedhyp,
                               b_type1,b_type2,bmi,ethrisk,fh_cvd,
                               rati, sbp,smoke_cat, surv, town,
                               errorBuf,errorBufSize){
    ok=1;
	  errorBuf=0;
	  if (!i_in_range(age, 25, 84)) {
		    ok=0;
		    strlcat(errorBuf,"error: age must be in range (25,84)\n",errorBufSize);
	  }
	  if (!is_boolean(b_AF)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_AF must be in range (0,1)\n",errorBufSize);
	  }
	  if (!is_boolean(b_ra)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_ra must be in range (0,1)\n",errorBufSize);
	  }
	  if (!is_boolean(b_renal)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_renal must be in range (0,1)\n",errorBufSize);
	  }
	  if (!is_boolean(b_treatedhyp)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_treatedhyp must be in range (0,1)\n",errorBufSize);
	  }
	  if (!is_boolean(b_type1)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_type1 must be in range (0,1)\n",errorBufSize);
	  }
	  if (!is_boolean(b_type2)) {
		    ok=0;
		    strlcat(errorBuf,"error: b_type2 must be in range (0,1)\n",errorBufSize);
	  }
	  if (!d_in_range(bmi,20,40)) {
		    ok=0;
		    strlcat(errorBuf,"error: bmi must be in range (20,40)\n",errorBufSize);
	  }
	  if (!i_in_range(ethrisk,1,9)) {
		    ok=0;
		    strlcat(errorBuf,"error: ethrisk must be in range (1,9)\n",errorBufSize);
	  }
	  if (!is_boolean(fh_cvd)) {
		    ok=0;
		    strlcat(errorBuf,"error: fh_cvd must be in range (0,1)\n",errorBufSize);
	  }
	  if (!d_in_range(rati,1,12)) {
		    ok=0;
		    strlcat(errorBuf,"error: rati must be in range (1,12)\n",errorBufSize);
	  }
	  if (!d_in_range(sbp,70,210)) {
		    ok=0;
		    strlcat(errorBuf,"error: sbp must be in range (70,210)\n",errorBufSize);
	  }
	  if (!i_in_range(smoke_cat,0,4)) {
		    ok=0;
		    strlcat(errorBuf,"error: smoke_cat must be in range (0,4)\n",errorBufSize);
	  }
    if (surv!=10) {
        ok=0;
        strlcat(errorBuf,"error: surv must be 10\n",errorBufSize);
    }
	  if (!d_in_range(town,-7,11)) {
		    ok=0;
		    strlcat(errorBuf,"error: town must be in range (-7,11)\n",errorBufSize);
	  }
	  return ok;
}
function cvd_female(age, b_AF, b_ra, b_renal, b_treatedhyp,
                    b_type1, b_type2, bmi, ethrisk,
                    fh_cvd, rati, sbp, smoke_cat, surv,
                    town, error, errorBuf, errorBufSize )
{
	  error = 0;
    
	  ok = cvd_female_validation(age, b_AF, b_ra, b_renal, b_treatedhyp,
                               b_type1, b_type2, bmi, ethrisk, fh_cvd,
                               rati, sbp, smoke_cat,surv,town,
                               errorBuf,errorBufSize);
	  if(!ok) {
		    error = 1;
		    return 0.0;
	  }
    
	  return cvd_female_raw(age,b_AF,b_ra,b_renal,
                          b_treatedhyp,b_type1,
                          b_type2,bmi,ethrisk,
                          fh_cvd,rati,sbp,smoke_cat,surv,town);
}
